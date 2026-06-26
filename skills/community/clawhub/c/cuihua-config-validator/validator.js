#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

class ConfigValidator {
  validate(file) {
    const content = fs.readFileSync(file, 'utf8');
    const ext = path.extname(file);
    
    if (ext === '.json') {
      try {
        JSON.parse(content);
        console.log('✅ Valid JSON');
      } catch (e) {
        console.log('❌ Invalid JSON:', e.message);
      }
    }
  }
}

export default ConfigValidator;

if (import.meta.url === \`file://\${process.argv[1]}\`) {
  const validator = new ConfigValidator();
  validator.validate(process.argv[2] || 'package.json');
}
