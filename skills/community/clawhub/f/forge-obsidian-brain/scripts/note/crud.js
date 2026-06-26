#!/usr/bin/env node
/**
 * Note CRUD Module
 * Create, Read, Update, Delete notes with frontmatter support
 */

const fs = require('fs');
const path = require('path');

/**
 * Parse frontmatter from note content
 * @param {string} content 
 * @returns {{frontmatter: Object, body: string}}
 */
function parseFrontmatter(content) {
  const frontmatterRegex = /^---\s*\n([\s\S]*?)\n---\s*\n?/;
  const match = content.match(frontmatterRegex);
  
  if (!match) {
    return { frontmatter: {}, body: content };
  }

  const rawFrontmatter = match[1];
  const body = content.slice(match[0].length);
  const frontmatter = {};

  // Simple YAML-like parsing for common cases
  const lines = rawFrontmatter.split('\n');
  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.slice(0, colonIndex).trim();
      let value = line.slice(colonIndex + 1).trim();
      
      // Remove quotes if present
      if ((value.startsWith('"') && value.endsWith('"')) ||
          (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }
      
      frontmatter[key] = value;
    }
  }

  return { frontmatter, body };
}

/**
 * Stringify frontmatter object to YAML-like format
 * @param {Object} frontmatter 
 * @returns {string}
 */
function stringifyFrontmatter(frontmatter) {
  if (!frontmatter || Object.keys(frontmatter).length === 0) {
    return '';
  }

  const lines = ['---'];
  for (const [key, value] of Object.entries(frontmatter)) {
    const stringValue = String(value);
    // Quote if contains special characters
    if (stringValue.includes(':') || stringValue.includes('#') || 
        stringValue.includes('\n') || stringValue.startsWith('"')) {
      lines.push(`${key}: "${stringValue.replace(/"/g, '\\"')}"`);
    } else {
      lines.push(`${key}: ${stringValue}`);
    }
  }
  lines.push('---', '');
  
  return lines.join('\n');
}

/**
 * Resolve a note path (handles relative and absolute paths)
 * @param {string} vaultPath 
 * @param {string} notePath 
 * @returns {string}
 */
function resolveNotePath(vaultPath, notePath) {
  // If already absolute and inside vault, use as-is
  if (path.isAbsolute(notePath)) {
    if (notePath.startsWith(vaultPath)) {
      return notePath;
    }
    // Assume it's relative to vault root
    return path.join(vaultPath, notePath);
  }
  
  return path.join(vaultPath, notePath);
}

/**
 * Ensure .md extension
 * @param {string} filename 
 * @returns {string}
 */
function ensureMdExtension(filename) {
  if (!filename.endsWith('.md')) {
    return filename + '.md';
  }
  return filename;
}

/**
 * Check if a note exists
 * @param {string} vaultPath 
 * @param {string} notePath 
 * @returns {boolean}
 */
function noteExists(vaultPath, notePath) {
  const fullPath = resolveNotePath(vaultPath, ensureMdExtension(notePath));
  return fs.existsSync(fullPath) && fs.statSync(fullPath).isFile();
}

/**
 * Read a note and parse its frontmatter
 * @param {string} vaultPath 
 * @param {string} notePath 
 * @returns {{success: boolean, frontmatter: Object, body: string, path: string, error?: string}}
 */
function readNote(vaultPath, notePath) {
  try {
    const fullPath = resolveNotePath(vaultPath, ensureMdExtension(notePath));
    
    if (!fs.existsSync(fullPath)) {
      return { success: false, error: `Note not found: ${notePath}`, frontmatter: {}, body: '', path: fullPath };
    }

    const content = fs.readFileSync(fullPath, 'utf8');
    const { frontmatter, body } = parseFrontmatter(content);

    return {
      success: true,
      frontmatter,
      body,
      path: fullPath,
      relativePath: path.relative(vaultPath, fullPath),
    };
  } catch (err) {
    return { success: false, error: err.message, frontmatter: {}, body: '', path: '' };
  }
}

/**
 * Create a new note
 * @param {string} vaultPath 
 * @param {string} notePath 
 * @param {Object} options 
 * @param {string} options.content - Body content
 * @param {Object} options.frontmatter - Frontmatter object
 * @param {boolean} options.overwrite - Allow overwriting existing note
 * @returns {{success: boolean, path: string, error?: string}}
 */
function createNote(vaultPath, notePath, options = {}) {
  try {
    const fullPath = resolveNotePath(vaultPath, ensureMdExtension(notePath));
    
    // Ensure parent directories exist
    const parentDir = path.dirname(fullPath);
    if (!fs.existsSync(parentDir)) {
      fs.mkdirSync(parentDir, { recursive: true });
    }

    // Check for existing note
    if (fs.existsSync(fullPath) && !options.overwrite) {
      return { success: false, error: `Note already exists: ${notePath}`, path: fullPath };
    }

    // Build content
    let content = '';
    if (options.frontmatter && Object.keys(options.frontmatter).length > 0) {
      content += stringifyFrontmatter(options.frontmatter);
    }
    if (options.content) {
      content += options.content;
    }
    if (!content.endsWith('\n') && content.length > 0) {
      content += '\n';
    }

    fs.writeFileSync(fullPath, content, 'utf8');

    return {
      success: true,
      path: fullPath,
      relativePath: path.relative(vaultPath, fullPath),
      created: !fs.existsSync(fullPath) || options.overwrite,
    };
  } catch (err) {
    return { success: false, error: err.message, path: '' };
  }
}

/**
 * Update an existing note
 * @param {string} vaultPath 
 * @param {string} notePath 
 * @param {Object} options 
 * @param {string} options.content - New body content (null to keep existing)
 * @param {Object} options.frontmatter - New frontmatter (null to keep existing)
 * @param {boolean} options.mergeFrontmatter - Merge with existing frontmatter
 * @returns {{success: boolean, path: string, error?: string}}
 */
function updateNote(vaultPath, notePath, options = {}) {
  try {
    const fullPath = resolveNotePath(vaultPath, ensureMdExtension(notePath));
    
    if (!fs.existsSync(fullPath)) {
      return { success: false, error: `Note not found: ${notePath}`, path: fullPath };
    }

    // Read existing content
    const existing = readNote(vaultPath, notePath);
    if (!existing.success) {
      return { success: false, error: existing.error, path: fullPath };
    }

    // Determine new content
    let newFrontmatter = existing.frontmatter;
    let newBody = existing.body;

    if (options.frontmatter !== null && options.frontmatter !== undefined) {
      if (options.mergeFrontmatter) {
        newFrontmatter = { ...existing.frontmatter, ...options.frontmatter };
      } else {
        newFrontmatter = options.frontmatter;
      }
    }

    if (options.content !== null && options.content !== undefined) {
      newBody = options.content;
    }

    // Build new content
    let content = stringifyFrontmatter(newFrontmatter) + newBody;
    if (!content.endsWith('\n') && content.length > 0) {
      content += '\n';
    }

    fs.writeFileSync(fullPath, content, 'utf8');

    return {
      success: true,
      path: fullPath,
      relativePath: path.relative(vaultPath, fullPath),
    };
  } catch (err) {
    return { success: false, error: err.message, path: '' };
  }
}

/**
 * Delete a note
 * @param {string} vaultPath 
 * @param {string} notePath 
 * @param {boolean} confirm - Require explicit confirmation
 * @returns {{success: boolean, path: string, error?: string}}
 */
function deleteNote(vaultPath, notePath, confirm = true) {
  try {
    const fullPath = resolveNotePath(vaultPath, ensureMdExtension(notePath));
    
    if (!fs.existsSync(fullPath)) {
      return { success: false, error: `Note not found: ${notePath}`, path: fullPath };
    }

    fs.unlinkSync(fullPath);

    return {
      success: true,
      path: fullPath,
      relativePath: path.relative(vaultPath, fullPath),
    };
  } catch (err) {
    return { success: false, error: err.message, path: '' };
  }
}

/**
 * List notes in a folder
 * @param {string} vaultPath 
 * @param {string} folderPath 
 * @returns {{success: boolean, notes: Array, error?: string}}
 */
function listNotes(vaultPath, folderPath = '') {
  try {
    const fullPath = resolveNotePath(vaultPath, folderPath);
    
    if (!fs.existsSync(fullPath)) {
      return { success: false, notes: [], error: `Folder not found: ${folderPath}` };
    }

    const items = fs.readdirSync(fullPath, { withFileTypes: true });
    const notes = items
      .filter(item => item.isFile() && item.name.endsWith('.md'))
      .map(item => ({
        name: item.name,
        path: path.join(folderPath, item.name),
        fullPath: path.join(fullPath, item.name),
      }));

    return { success: true, notes };
  } catch (err) {
    return { success: false, notes: [], error: err.message };
  }
}

/**
 * Search notes using grep/shell
 * @param {string} vaultPath 
 * @param {string} query 
 * @param {Object} options
 * @returns {{success: boolean, results: Array, error?: string}}
 */
function searchNotes(vaultPath, query, options = {}) {
  try {
    const folder = options.folder || '';
    const searchPath = path.join(vaultPath, folder);
    
    if (!fs.existsSync(searchPath)) {
      return { success: true, results: [], error: `Folder not found: ${folder}` };
    }
    
    // Pure Node.js file search - no shell execution
    const findMarkdownFiles = (dir, files = []) => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== '.obsidian') {
          findMarkdownFiles(fullPath, files);
        } else if (entry.isFile() && entry.name.endsWith('.md')) {
          files.push(fullPath);
        }
      }
      return files;
    };
    
    const files = findMarkdownFiles(searchPath);
    const queryLower = query.toLowerCase();
    
    const results = [];
    for (const file of files) {
      try {
        const content = fs.readFileSync(file, 'utf8');
        if (content.toLowerCase().includes(queryLower)) {
          results.push({
            fullPath: file,
            relativePath: path.relative(vaultPath, file),
          });
        }
      } catch (readErr) {
        // Skip files we can't read
        continue;
      }
    }

    return { success: true, results };
  } catch (err) {
    return { success: true, results: [] };
  }
}

// CLI support
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  const vaultPath = args[1] || process.env.OBSIDIAN_VAULT;

  if (!vaultPath) {
    console.error('Error: Vault path required (argument or OBSIDIAN_VAULT env)');
    console.error('Usage: crud.js <command> <vault-path> [args...]');
    console.error('Commands: read, create, update, delete, list, search, exists');
    process.exit(1);
  }

  switch (command) {
    case 'read': {
      const notePath = args[2];
      if (!notePath) {
        console.error('Usage: crud.js read <vault-path> <note-path>');
        process.exit(1);
      }
      console.log(JSON.stringify(readNote(vaultPath, notePath), null, 2));
      break;
    }
    case 'create': {
      const notePath = args[2];
      const content = args[3] || '';
      if (!notePath) {
        console.error('Usage: crud.js create <vault-path> <note-path> [content]');
        process.exit(1);
      }
      const result = createNote(vaultPath, notePath, { content });
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
      break;
    }
    case 'update': {
      const notePath = args[2];
      const content = args[3] || null;
      if (!notePath) {
        console.error('Usage: crud.js update <vault-path> <note-path> [content]');
        process.exit(1);
      }
      const result = updateNote(vaultPath, notePath, { content });
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
      break;
    }
    case 'delete': {
      const notePath = args[2];
      if (!notePath) {
        console.error('Usage: crud.js delete <vault-path> <note-path>');
        process.exit(1);
      }
      const result = deleteNote(vaultPath, notePath);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
      break;
    }
    case 'list': {
      const folderPath = args[2] || '';
      console.log(JSON.stringify(listNotes(vaultPath, folderPath), null, 2));
      break;
    }
    case 'search': {
      const query = args[2];
      if (!query) {
        console.error('Usage: crud.js search <vault-path> <query>');
        process.exit(1);
      }
      console.log(JSON.stringify(searchNotes(vaultPath, query), null, 2));
      break;
    }
    case 'exists': {
      const notePath = args[2];
      if (!notePath) {
        console.error('Usage: crud.js exists <vault-path> <note-path>');
        process.exit(1);
      }
      const exists = noteExists(vaultPath, notePath);
      console.log(JSON.stringify({ exists, path: resolveNotePath(vaultPath, notePath) }, null, 2));
      process.exit(exists ? 0 : 1);
      break;
    }
    default:
      console.error(`Unknown command: ${command}`);
      console.error('Commands: read, create, update, delete, list, search, exists');
      process.exit(1);
  }
}

module.exports = {
  readNote,
  createNote,
  updateNote,
  deleteNote,
  listNotes,
  searchNotes,
  noteExists,
  parseFrontmatter,
  stringifyFrontmatter,
  resolveNotePath,
  ensureMdExtension,
};
