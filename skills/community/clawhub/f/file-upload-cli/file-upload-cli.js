#!/usr/bin/env node

const { execFile } = require('child_process');
const { promisify } = require('util');
const fs = require('fs').promises;
const fsSync = require('fs');
const path = require('path');

const execFileAsync = promisify(execFile);

// Exit code constants
const EXIT_SUCCESS = 0;
const EXIT_GENERAL_ERROR = 1;
const EXIT_NETWORK_ERROR = 2;
const EXIT_SERVICE_ERROR = 3;
const EXIT_VALIDATION_ERROR = 4;

// Main execution function
async function main() {
  try {
    // T006: Parse CLI argument
    const filePathArg = process.argv[2];
    
    // T008: Resolve file path
    const filePath = filePathArg ? path.resolve(filePathArg) : null;
    
    if (!filePath) {
      console.error('Error: No file path provided');
      console.error('Usage: node file-upload-cli.js <filePath>');
      process.exit(EXIT_VALIDATION_ERROR);
    }
    
    // T010: Validate file existence
    try {
      await fs.access(filePath, fsSync.constants.R_OK);
    } catch (error) {
      console.error(`Error: File not found - ${filePath}`);
      console.error('Please check the file path and try again.');
      process.exit(EXIT_VALIDATION_ERROR);
    }
    
    // T011: Check if path is a file (not directory)
    const stats = await fs.stat(filePath);
    if (!stats.isFile()) {
      console.error(`Error: Path is a directory - ${filePath}`);
      console.error('Please provide a file path, not a directory.');
      process.exit(EXIT_VALIDATION_ERROR);
    }
    
    // T012: Check file size (1GB limit)
    const MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024; // 1GB in bytes
    if (stats.size > MAX_FILE_SIZE) {
      const sizeGB = (stats.size / (1024 * 1024 * 1024)).toFixed(2);
      console.error(`Error: File too large - ${sizeGB} GB (limit: 1 GB)`);
      console.error('The file exceeds the litterbox.catbox.moe service limit.');
      process.exit(EXIT_VALIDATION_ERROR);
    }
    
    // Check for empty file
    if (stats.size === 0) {
      console.error(`Error: File is empty - ${filePath}`);
      console.error('Cannot upload an empty file.');
      process.exit(EXIT_VALIDATION_ERROR);
    }
    
    // T013-T016: Upload using curl
    console.log('Uploading...');
    
    // T014: Execute curl command (use curl.exe on Windows to avoid PowerShell alias)
    const curlCmd = process.platform === 'win32' ? 'curl.exe' : 'curl';
    const { stdout, stderr } = await execFileAsync(curlCmd, [
      '-F', 'reqtype=fileupload',
      '-F', 'time=72h',
      '-F', `fileToUpload=@${filePath}`,
      'https://litterbox.catbox.moe/resources/internals/api.php'
    ], {
      maxBuffer: 1024 * 1024 * 10, // 10MB buffer
      timeout: 60000 // 60 second timeout
    });
    
    // T017: Parse response and extract URL
    const url = stdout.trim();
    
    // T018: Display success message
    console.log('File uploaded successfully!');
    console.log(`URL: ${url}`);
    console.log('Note: File will be available for 72 hours.');
    
    // T019: Exit with success code
    process.exit(EXIT_SUCCESS);
    
  } catch (error) {
    // Handle curl execution errors
    if (error.code === 'ENOENT') {
      console.error('Error: curl command not found');
      console.error('Please install curl to use this tool.');
      process.exit(EXIT_GENERAL_ERROR);
    }
    
    if (error.killed && error.signal === 'SIGTERM') {
      console.error('Error: Connection timeout');
      console.error('The upload request timed out. Please try again.');
      process.exit(EXIT_NETWORK_ERROR);
    }
    
    // Check stderr for curl errors
    if (error.stderr) {
      const stderr = error.stderr.toLowerCase();
      if (stderr.includes('could not resolve host') || 
          stderr.includes('connection refused') || 
          stderr.includes('could not connect') ||
          stderr.includes('failed to connect')) {
        console.error('Error: Network error - Cannot connect to litterbox.catbox.moe');
        console.error('Please check your internet connection and try again.');
        process.exit(EXIT_NETWORK_ERROR);
      }
      if (stderr.includes('timeout') || stderr.includes('timed out')) {
        console.error('Error: Connection timeout');
        console.error('The upload request timed out. Please try again.');
        process.exit(EXIT_NETWORK_ERROR);
      }
    }
    
    // Check for HTTP error codes in stderr
    if (error.code !== 0 && error.stderr) {
      const stderr = error.stderr;
      if (stderr.includes('413')) {
        console.error('Error: Service error - File too large (413)');
        console.error('The litterbox.catbox.moe service rejected the file. Maximum size is 1 GB.');
        process.exit(EXIT_SERVICE_ERROR);
      } else if (stderr.includes('500')) {
        console.error('Error: Service error - Internal server error (500)');
        console.error('The litterbox.catbox.moe service encountered an error. Please try again later.');
        process.exit(EXIT_SERVICE_ERROR);
      } else if (stderr.includes('502') || stderr.includes('503')) {
        console.error('Error: Service unavailable');
        console.error('The litterbox.catbox.moe service is temporarily unavailable. Please try again later.');
        process.exit(EXIT_SERVICE_ERROR);
      }
    }
    
    // General error fallback
    console.error('Error:', error.message || 'Upload failed');
    if (error.stderr) {
      console.error('Details:', error.stderr);
    }
    process.exit(EXIT_GENERAL_ERROR);
  }
}

// Execute main function
main();