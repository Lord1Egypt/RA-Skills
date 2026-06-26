#!/usr/bin/env node

/**
 * Code Runner Script for Agent Skills
 * 
 * Executes code snippets in various programming languages.
 * 
 * Usage: node run-code.js <languageId> "<code>"
 * 
 * Example: node run-code.js javascript "console.log('Hello, World!')"
 */

const { exec, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Configuration: Language ID to executor mapping
const languageConfig = {
    // Interpreted Languages
    javascript: { executor: 'node', ext: 'js' },
    typescript: { executor: 'ts-node', ext: 'ts' },
    python: { executor: 'python -u', ext: 'py' },
    ruby: { executor: 'ruby', ext: 'rb' },
    php: { executor: 'php', ext: 'php' },
    perl: { executor: 'perl', ext: 'pl' },
    perl6: { executor: 'perl6', ext: 'p6' },
    lua: { executor: 'lua', ext: 'lua' },
    r: { executor: 'Rscript', ext: 'r' },
    julia: { executor: 'julia', ext: 'jl' },
    groovy: { executor: 'groovy', ext: 'groovy' },
    kotlin: { executor: 'kotlin', ext: 'kts', isScript: true },
    scala: { executor: 'scala', ext: 'scala' },
    swift: { executor: 'swift', ext: 'swift' },
    dart: { executor: 'dart run', ext: 'dart' },
    elixir: { executor: 'elixir', ext: 'exs' },
    clojure: { executor: 'clojure', ext: 'clj' },
    racket: { executor: 'racket', ext: 'rkt' },
    scheme: { executor: 'scheme --script', ext: 'scm' },
    lisp: { executor: 'sbcl --script', ext: 'lisp' },
    ocaml: { executor: 'ocaml', ext: 'ml' },
    haskell: { executor: 'runhaskell', ext: 'hs' },
    crystal: { executor: 'crystal run', ext: 'cr' },
    nim: { executor: 'nim compile --verbosity:0 --hints:off --run', ext: 'nim' },
    coffeescript: { executor: 'coffee', ext: 'coffee' },
    
    // Shell/Script Languages
    shellscript: { executor: 'bash', ext: 'sh' },
    bash: { executor: 'bash', ext: 'sh' },
    powershell: { executor: process.platform === 'win32' ? 'powershell -ExecutionPolicy ByPass -File' : 'pwsh -File', ext: 'ps1' },
    bat: { executor: 'cmd /c', ext: 'bat' },
    cmd: { executor: 'cmd /c', ext: 'cmd' },
    
    // .NET Languages
    fsharp: { executor: 'dotnet fsi', ext: 'fsx' },
    csharp: { executor: 'dotnet script', ext: 'csx' },
    vbscript: { executor: 'cscript //Nologo', ext: 'vbs' },
    
    // Compiled Languages (compile and run)
    c: { 
        ext: 'c',
        compile: true,
        compileCmd: (src, out) => `gcc "${src}" -o "${out}"`,
        runCmd: (out) => `"${out}"`
    },
    cpp: { 
        ext: 'cpp',
        compile: true,
        compileCmd: (src, out) => `g++ "${src}" -o "${out}"`,
        runCmd: (out) => `"${out}"`
    },
    java: {
        ext: 'java',
        compile: true,
        // Java requires class name to match filename
        compileCmd: (src, out, dir) => `javac "${src}"`,
        runCmd: (out, dir, className) => `java -cp "${dir}" ${className}`,
        extractClassName: true
    },
    go: { executor: 'go run', ext: 'go' },
    rust: {
        ext: 'rs',
        compile: true,
        compileCmd: (src, out) => `rustc "${src}" -o "${out}"`,
        runCmd: (out) => `"${out}"`
    },
    
    // Other Languages
    applescript: { executor: 'osascript', ext: 'applescript' },
    ahk: { executor: 'autohotkey', ext: 'ahk' },
    autoit: { executor: 'autoit3', ext: 'au3' },
    sass: { executor: 'sass --style expanded', ext: 'sass' },
    scss: { executor: 'sass --style expanded', ext: 'scss' },
};

// Default timeout in milliseconds (30 seconds)
const DEFAULT_TIMEOUT = 30000;

/**
 * Create a temporary file with the code content
 */
function createTempFile(code, ext, customName = null) {
    const tmpDir = os.tmpdir();
    const fileName = customName || `code_runner_${Date.now()}`;
    const filePath = path.join(tmpDir, `${fileName}.${ext}`);
    fs.writeFileSync(filePath, code, 'utf8');
    return filePath;
}

/**
 * Clean up temporary files
 */
function cleanupFiles(...files) {
    for (const file of files) {
        try {
            if (fs.existsSync(file)) {
                fs.unlinkSync(file);
            }
        } catch (e) {
            // Ignore cleanup errors
        }
    }
}

/**
 * Extract Java class name from code
 */
function extractJavaClassName(code) {
    const match = code.match(/public\s+class\s+(\w+)/);
    return match ? match[1] : 'Main';
}

/**
 * Execute a command with timeout
 */
function executeCommand(command, timeout = DEFAULT_TIMEOUT) {
    return new Promise((resolve, reject) => {
        const startTime = Date.now();
        
        const child = exec(command, {
            timeout: timeout,
            maxBuffer: 10 * 1024 * 1024, // 10MB buffer
            encoding: 'utf8'
        }, (error, stdout, stderr) => {
            const duration = Date.now() - startTime;
            
            if (error) {
                if (error.killed) {
                    reject({
                        error: 'Execution timed out',
                        duration,
                        stderr: stderr || ''
                    });
                } else {
                    reject({
                        error: error.message,
                        duration,
                        stderr: stderr || '',
                        code: error.code
                    });
                }
                return;
            }
            
            resolve({
                stdout: stdout || '',
                stderr: stderr || '',
                duration
            });
        });
    });
}

/**
 * Run code in the specified language
 */
async function runCode(languageId, code, options = {}) {
    const lang = languageId.toLowerCase();
    const config = languageConfig[lang];
    
    if (!config) {
        const supported = Object.keys(languageConfig).join(', ');
        throw new Error(`Unsupported language: ${languageId}\n\nSupported languages: ${supported}`);
    }
    
    const timeout = options.timeout || DEFAULT_TIMEOUT;
    let tempFile = null;
    let outputFile = null;
    
    try {
        // Handle compiled languages
        if (config.compile) {
            const tmpDir = os.tmpdir();
            
            // Special handling for Java
            if (lang === 'java') {
                const className = extractJavaClassName(code);
                tempFile = createTempFile(code, config.ext, className);
                const dir = path.dirname(tempFile);
                
                // Compile
                const compileCmd = config.compileCmd(tempFile, null, dir);
                await executeCommand(compileCmd, timeout);
                
                // Run
                const runCmd = config.runCmd(null, dir, className);
                const result = await executeCommand(runCmd, timeout);
                
                // Cleanup class file
                cleanupFiles(path.join(dir, `${className}.class`));
                
                return result;
            }
            
            // Other compiled languages (C, C++, Rust)
            tempFile = createTempFile(code, config.ext);
            outputFile = path.join(tmpDir, `code_runner_${Date.now}${process.platform === 'win32' ? '.exe' : ''}`);
            
            // Compile
            const compileCmd = config.compileCmd(tempFile, outputFile);
            await executeCommand(compileCmd, timeout);
            
            // Run
            const runCmd = config.runCmd(outputFile);
            return await executeCommand(runCmd, timeout);
        }
        
        // Handle interpreted languages
        tempFile = createTempFile(code, config.ext);
        const command = `${config.executor} "${tempFile}"`;
        
        return await executeCommand(command, timeout);
        
    } finally {
        // Cleanup
        if (tempFile) cleanupFiles(tempFile);
        if (outputFile) cleanupFiles(outputFile);
    }
}

/**
 * Format output for display
 */
function formatOutput(result) {
    let output = '';
    
    if (result.stdout) {
        output += result.stdout;
    }
    
    if (result.stderr) {
        if (output) output += '\n';
        output += `[stderr]: ${result.stderr}`;
    }
    
    return output || '(no output)';
}

/**
 * Format error for display
 */
function formatError(error) {
    let message = `Error: ${error.error || error.message || 'Unknown error'}`;
    
    if (error.stderr) {
        message += `\n${error.stderr}`;
    }
    
    if (error.code !== undefined) {
        message += `\n(exit code: ${error.code})`;
    }
    
    return message;
}

/**
 * Read from stdin
 */
function readStdin() {
    return new Promise((resolve) => {
        let data = '';
        process.stdin.setEncoding('utf8');
        process.stdin.on('data', (chunk) => {
            data += chunk;
        });
        process.stdin.on('end', () => {
            resolve(data);
        });
    });
}

// Main execution
async function main() {
    const args = process.argv.slice(2);
    
    // Show help if no arguments
    if (args.length === 0) {
        console.log('Code Runner - Execute code snippets in various languages\n');
        console.log('Usage (recommended for AI agents - avoids escaping issues):');
        console.log('  echo "<code>" | node run-code.cjs <languageId> [--timeout <ms>]');
        console.log('  node run-code.cjs <languageId> [--timeout <ms>] < code_file.ext\n');
        console.log('Usage (CLI arguments - for simple manual testing):');
        console.log('  node run-code.cjs <languageId> "<code>" [--timeout <ms>]\n');
        console.log('Examples:');
        console.log('  echo "console.log(\'Hello!\')" | node run-code.cjs javascript');
        console.log('  echo "print(\'Hello!\')" | node run-code.cjs python');
        console.log('  node run-code.cjs javascript "console.log(5 + 3)"\n');
        console.log('Supported languages:');
        console.log('  ' + Object.keys(languageConfig).join(', '));
        process.exit(1);
    }
    
    const languageId = args[0];
    
    // Parse optional timeout
    let timeout = DEFAULT_TIMEOUT;
    const timeoutIndex = args.indexOf('--timeout');
    if (timeoutIndex !== -1 && args[timeoutIndex + 1]) {
        timeout = parseInt(args[timeoutIndex + 1], 10);
    }
    
    // Determine if code comes from stdin or CLI argument
    let code;
    const isStdin = !process.stdin.isTTY; // stdin is piped
    
    if (isStdin) {
        // Read code from stdin (recommended for AI agents)
        code = await readStdin();
        if (!code || code.trim().length === 0) {
            console.error('Error: No code provided via stdin');
            process.exit(1);
        }
    } else {
        // Read code from CLI argument (for manual testing)
        if (args.length < 2) {
            console.error('Error: No code provided. Use stdin (recommended) or pass code as argument.');
            console.error('Examples:');
            console.error('  echo "code" | node run-code.cjs <language>');
            console.error('  node run-code.cjs <language> "code"');
            process.exit(1);
        }
        code = args[1];
    }
    
    try {
        const result = await runCode(languageId, code, { timeout });
        console.log(formatOutput(result));
        process.exit(0);
    } catch (error) {
        console.error(formatError(error));
        process.exit(1);
    }
}

// Export for programmatic use
module.exports = { runCode, languageConfig };

// Run if executed directly
if (require.main === module) {
    main();
}
