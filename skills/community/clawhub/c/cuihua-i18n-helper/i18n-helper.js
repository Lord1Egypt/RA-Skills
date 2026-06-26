#!/usr/bin/env node

/**
 * cuihua-i18n-helper - AI-Powered i18n Assistant
 * Core engine for string extraction, translation, and quality checks
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class I18nHelper {
  constructor(options = {}) {
    this.options = {
      sourceLanguage: options.sourceLanguage || 'en',
      targetLanguages: options.targetLanguages || ['zh', 'ja'],
      localesPath: options.localesPath || './locales',
      extractFrom: options.extractFrom || ['./src'],
      keyStyle: options.keyStyle || 'nested',
      placeholderPattern: options.placeholderPattern || '{{%s}}',
      ...options
    };
    
    this.strings = new Map();
    this.translations = {};
    this.stats = {
      filesScanned: 0,
      stringsFound: 0,
      translationsGenerated: 0,
      issues: []
    };
  }

  /**
   * Extract translatable strings from code
   */
  async extractStrings(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const ext = path.extname(filePath);
    
    this.stats.filesScanned++;

    // Extract based on file type
    if (['.jsx', '.tsx', '.js', '.ts'].includes(ext)) {
      this.extractFromJSX(content, filePath);
    } else if (['.vue'].includes(ext)) {
      this.extractFromVue(content, filePath);
    } else if (['.html'].includes(ext)) {
      this.extractFromHTML(content, filePath);
    }
  }

  /**
   * Extract from JSX/React
   */
  extractFromJSX(content, filePath) {
    // Pattern 1: JSX text content <tag>Text</tag>
    const jsxTextPattern = />([^<>{}\n]+)</g;
    let match;
    
    while ((match = jsxTextPattern.exec(content)) !== null) {
      const text = match[1].trim();
      if (this.isTranslatable(text)) {
        const key = this.generateKey(text, filePath);
        this.addString(key, text, filePath, match.index);
      }
    }

    // Pattern 2: String literals in JSX attributes
    const attrPattern = /(?:placeholder|title|alt|label|aria-label)=['"]([^'"]+)['"]/g;
    while ((match = attrPattern.exec(content)) !== null) {
      const text = match[1].trim();
      if (this.isTranslatable(text)) {
        const key = this.generateKey(text, filePath);
        this.addString(key, text, filePath, match.index);
      }
    }

    // Pattern 3: Hardcoded strings in JavaScript
    const stringPattern = /['"]([A-Z][^'"]{3,})['"]/g;
    while ((match = stringPattern.exec(content)) !== null) {
      const text = match[1].trim();
      if (this.isTranslatable(text) && !this.isCode(text)) {
        const key = this.generateKey(text, filePath);
        this.addString(key, text, filePath, match.index);
      }
    }
  }

  /**
   * Extract from Vue templates
   */
  extractFromVue(content, filePath) {
    // Vue template section
    const templateMatch = content.match(/<template>([\s\S]*?)<\/template>/);
    if (templateMatch) {
      const template = templateMatch[1];
      
      // Extract from template text
      const textPattern = />([^<>{}\n]+)</g;
      let match;
      
      while ((match = textPattern.exec(template)) !== null) {
        const text = match[1].trim();
        if (this.isTranslatable(text)) {
          const key = this.generateKey(text, filePath);
          this.addString(key, text, filePath, match.index);
        }
      }

      // Extract from attributes
      const attrPattern = /(?:placeholder|title|alt|label)=['"]([^'"]+)['"]/g;
      while ((match = attrPattern.exec(template)) !== null) {
        const text = match[1].trim();
        if (this.isTranslatable(text)) {
          const key = this.generateKey(text, filePath);
          this.addString(key, text, filePath, match.index);
        }
      }
    }
  }

  /**
   * Extract from HTML
   */
  extractFromHTML(content, filePath) {
    const textPattern = />([^<>{}]+)</g;
    let match;
    
    while ((match = textPattern.exec(content)) !== null) {
      const text = match[1].trim();
      if (this.isTranslatable(text)) {
        const key = this.generateKey(text, filePath);
        this.addString(key, text, filePath, match.index);
      }
    }
  }

  /**
   * Check if text is translatable
   */
  isTranslatable(text) {
    // Too short
    if (text.length < 2) return false;
    
    // Only whitespace
    if (!/\S/.test(text)) return false;
    
    // Only numbers or symbols
    if (!/[a-zA-Z]/.test(text)) return false;
    
    // Already a translation key
    if (/^[a-z_]+\.[a-z_]+/.test(text)) return false;
    
    // Code-like patterns
    if (/^[A-Z_]+$/.test(text)) return false; // CONSTANT
    if (/^[a-z]+[A-Z]/.test(text)) return false; // camelCase
    if (/^\./.test(text) || /\(\)/.test(text)) return false; // .method() or function()
    
    return true;
  }

  /**
   * Check if text looks like code
   */
  isCode(text) {
    const codePatterns = [
      /^import\s/,
      /^export\s/,
      /^const\s/,
      /^let\s/,
      /^var\s/,
      /^function\s/,
      /^class\s/,
      /^\w+\(/,  // function calls
      /^\./,     // method calls
    ];
    
    return codePatterns.some(pattern => pattern.test(text));
  }

  /**
   * Generate translation key from text
   */
  generateKey(text, filePath) {
    // Extract component/file name
    const fileName = path.basename(filePath, path.extname(filePath));
    const component = fileName.toLowerCase().replace(/[^a-z0-9]/g, '_');
    
    // Generate key from text
    let key = text
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, '')
      .trim()
      .split(/\s+/)
      .slice(0, 4)
      .join('_');
    
    // Categorize by context
    let category = 'common';
    if (/button|btn|submit|cancel|save|delete/i.test(fileName)) {
      category = 'button';
    } else if (/form|input|field/i.test(fileName)) {
      category = 'form';
    } else if (/error|warning|alert/i.test(fileName)) {
      category = 'error';
    } else if (/nav|menu|header|footer/i.test(fileName)) {
      category = 'navigation';
    }
    
    return `${category}.${key}`;
  }

  /**
   * Add string to collection
   */
  addString(key, text, filePath, position) {
    if (!this.strings.has(key)) {
      this.strings.set(key, {
        text,
        sources: []
      });
      this.stats.stringsFound++;
    }
    
    this.strings.get(key).sources.push({
      file: filePath,
      position
    });
  }

  /**
   * Generate locale files
   */
  generateLocaleFiles() {
    const locales = {};
    
    // Source language
    locales[this.options.sourceLanguage] = {};
    
    // Convert flat strings to nested structure
    this.strings.forEach((data, key) => {
      this.setNestedValue(
        locales[this.options.sourceLanguage],
        key,
        data.text
      );
    });

    // Create locales directory
    if (!fs.existsSync(this.options.localesPath)) {
      fs.mkdirSync(this.options.localesPath, { recursive: true });
    }

    // Write source language file
    const sourcePath = path.join(
      this.options.localesPath,
      `${this.options.sourceLanguage}.json`
    );
    fs.writeFileSync(sourcePath, JSON.stringify(locales[this.options.sourceLanguage], null, 2));

    // Create empty target language files
    this.options.targetLanguages.forEach(lang => {
      const targetPath = path.join(this.options.localesPath, `${lang}.json`);
      if (!fs.existsSync(targetPath)) {
        fs.writeFileSync(targetPath, JSON.stringify(locales[this.options.sourceLanguage], null, 2));
      }
    });

    return locales;
  }

  /**
   * Set nested object value from dot notation key
   */
  setNestedValue(obj, key, value) {
    const keys = key.split('.');
    let current = obj;
    
    for (let i = 0; i < keys.length - 1; i++) {
      if (!(keys[i] in current)) {
        current[keys[i]] = {};
      }
      current = current[keys[i]];
    }
    
    current[keys[keys.length - 1]] = value;
  }

  /**
   * Get nested object value from dot notation key
   */
  getNestedValue(obj, key) {
    const keys = key.split('.');
    let current = obj;
    
    for (const k of keys) {
      if (current && k in current) {
        current = current[k];
      } else {
        return undefined;
      }
    }
    
    return current;
  }

  /**
   * Check for missing translations
   */
  checkMissingTranslations() {
    const missing = {};
    
    this.options.targetLanguages.forEach(lang => {
      const targetPath = path.join(this.options.localesPath, `${lang}.json`);
      
      if (!fs.existsSync(targetPath)) {
        missing[lang] = Array.from(this.strings.keys());
        return;
      }
      
      const targetLocale = JSON.parse(fs.readFileSync(targetPath, 'utf8'));
      const missingKeys = [];
      
      this.strings.forEach((data, key) => {
        const value = this.getNestedValue(targetLocale, key);
        const sourceValue = data.text;
        
        // Check if missing or same as source (untranslated)
        if (!value || value === sourceValue) {
          missingKeys.push(key);
        }
      });
      
      if (missingKeys.length > 0) {
        missing[lang] = missingKeys;
      }
    });
    
    return missing;
  }

  /**
   * Check for unused translations
   */
  checkUnusedTranslations() {
    const unused = {};
    const usedKeys = new Set(this.strings.keys());
    
    [this.options.sourceLanguage, ...this.options.targetLanguages].forEach(lang => {
      const localePath = path.join(this.options.localesPath, `${lang}.json`);
      
      if (!fs.existsSync(localePath)) return;
      
      const locale = JSON.parse(fs.readFileSync(localePath, 'utf8'));
      const allKeys = this.getAllKeys(locale);
      const unusedKeys = allKeys.filter(key => !usedKeys.has(key));
      
      if (unusedKeys.length > 0) {
        unused[lang] = unusedKeys;
      }
    });
    
    return unused;
  }

  /**
   * Get all keys from nested object
   */
  getAllKeys(obj, prefix = '') {
    const keys = [];
    
    for (const key in obj) {
      const fullKey = prefix ? `${prefix}.${key}` : key;
      
      if (typeof obj[key] === 'object' && obj[key] !== null) {
        keys.push(...this.getAllKeys(obj[key], fullKey));
      } else {
        keys.push(fullKey);
      }
    }
    
    return keys;
  }

  /**
   * Generate report
   */
  generateReport() {
    const missing = this.checkMissingTranslations();
    const unused = this.checkUnusedTranslations();
    
    let report = `\n🌍 i18n Analysis Report\n`;
    report += `━`.repeat(50) + `\n\n`;
    report += `📁 Files scanned: ${this.stats.filesScanned}\n`;
    report += `📝 Translatable strings found: ${this.stats.stringsFound}\n`;
    report += `🌐 Target languages: ${this.options.targetLanguages.join(', ')}\n\n`;

    // Coverage
    report += `📊 Translation Coverage:\n`;
    const totalKeys = this.strings.size;
    
    [this.options.sourceLanguage, ...this.options.targetLanguages].forEach(lang => {
      const missingCount = missing[lang]?.length || 0;
      const coverage = totalKeys > 0 
        ? Math.round(((totalKeys - missingCount) / totalKeys) * 100)
        : 100;
      
      const icon = coverage === 100 ? '✅' : coverage >= 90 ? '⚠️' : '❌';
      report += `  ${icon} ${lang}: ${coverage}% (${totalKeys - missingCount}/${totalKeys})\n`;
    });
    
    // Missing translations
    if (Object.keys(missing).length > 0) {
      report += `\n❌ Missing Translations:\n`;
      for (const [lang, keys] of Object.entries(missing)) {
        report += `\n  ${lang} (${keys.length} missing):\n`;
        keys.slice(0, 5).forEach(key => {
          report += `    - ${key}\n`;
        });
        if (keys.length > 5) {
          report += `    ... and ${keys.length - 5} more\n`;
        }
      }
    } else {
      report += `\n✅ No missing translations!\n`;
    }

    // Unused translations
    if (Object.keys(unused).length > 0) {
      report += `\n🗑️  Unused Translations:\n`;
      for (const [lang, keys] of Object.entries(unused)) {
        report += `\n  ${lang} (${keys.length} unused):\n`;
        keys.slice(0, 5).forEach(key => {
          report += `    - ${key}\n`;
        });
        if (keys.length > 5) {
          report += `    ... and ${keys.length - 5} more\n`;
        }
      }
    }

    report += `\n💡 Next steps:\n`;
    if (Object.keys(missing).length > 0) {
      report += `  - Run translation to fill missing strings\n`;
    }
    if (Object.keys(unused).length > 0) {
      report += `  - Clean up unused translations\n`;
    }
    if (Object.keys(missing).length === 0 && Object.keys(unused).length === 0) {
      report += `  - Everything looks good! 🎉\n`;
    }
    
    return report;
  }

  /**
   * Scan directory recursively
   */
  scanDirectory(dir) {
    const files = fs.readdirSync(dir);
    
    files.forEach(file => {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);
      
      if (stat.isDirectory()) {
        if (!file.startsWith('.') && file !== 'node_modules' && file !== 'dist' && file !== 'build') {
          this.scanDirectory(filePath);
        }
      } else if (stat.isFile()) {
        const ext = path.extname(file);
        if (['.js', '.jsx', '.ts', '.tsx', '.vue', '.html'].includes(ext)) {
          this.extractStrings(filePath);
        }
      }
    });
  }
}

export default I18nHelper;

// CLI usage
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const command = args[0] || 'extract';
  const targetPath = args[1] || './src';
  
  const helper = new I18nHelper({
    sourceLanguage: 'en',
    targetLanguages: ['zh', 'ja'],
    localesPath: './locales'
  });
  
  console.log('🌍 cuihua-i18n-helper starting...\n');
  
  if (command === 'extract') {
    // Extract strings
    if (fs.statSync(targetPath).isDirectory()) {
      helper.scanDirectory(targetPath);
    } else {
      helper.extractStrings(targetPath);
    }
    
    // Generate locale files
    helper.generateLocaleFiles();
    
    // Show report
    console.log(helper.generateReport());
    
    console.log(`\n✅ Extraction complete!`);
    console.log(`📁 Locale files: ./locales/`);
    
  } else if (command === 'check') {
    // Load existing locales
    const sourcePath = path.join(helper.options.localesPath, `${helper.options.sourceLanguage}.json`);
    if (fs.existsSync(sourcePath)) {
      const sourceLocale = JSON.parse(fs.readFileSync(sourcePath, 'utf8'));
      const keys = helper.getAllKeys(sourceLocale);
      keys.forEach(key => {
        const value = helper.getNestedValue(sourceLocale, key);
        helper.addString(key, value, 'existing', 0);
      });
    }
    
    // Show report
    console.log(helper.generateReport());
  }
}
