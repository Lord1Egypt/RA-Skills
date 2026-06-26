const WordExtractor = require('word-extractor');

/**
 * Extract footnotes, endnotes, and body text from docx file
 * @param {string} filePath Path to the docx file
 * @returns {Promise<{body:string, footnotes:string[], endnotes:string[]}>}
 */
async function extractFootnotes(filePath) {
  const extractor = new WordExtractor();
  const doc = await extractor.extract(filePath);

  // Get footnotes (word-extractor returns string, need to split)
  const footnotesStr = doc.getFootnotes();
  let footnotes = [];
  if (footnotesStr && typeof footnotesStr === 'string') {
    // Split by newline, filter empty lines
    footnotes = footnotesStr
      .split('\n')
      .map(s => s.trim())
      .filter(Boolean);
  } else if (Array.isArray(footnotesStr)) {
    footnotes = footnotesStr.map(s => s.trim()).filter(Boolean);
  }

  // Get endnotes
  const endnotesStr = doc.getEndnotes();
  let endnotes = [];
  if (endnotesStr && typeof endnotesStr === 'string') {
    endnotes = endnotesStr
      .split('\n')
      .map(s => s.trim())
      .filter(Boolean);
  } else if (Array.isArray(endnotesStr)) {
    endnotes = endnotesStr.map(s => s.trim()).filter(Boolean);
  }

  return {
    body: doc.getBody().trim(),
    footnotes,
    endnotes,
  };
}

/**
 * Command line interface
 */
async function cli() {
  const file = process.argv[2];
  if (!file) {
    console.log('Usage: node index.js your.docx');
    process.exit(1);
  }

  try {
    const result = await extractFootnotes(file);
    
    console.log('========================================');
    console.log('Extraction Result');
    console.log('========================================\n');
    
    console.log(`Body length: ${result.body.length} characters\n`);
    console.log(`Footnotes count: ${result.footnotes.length}\n`);
    
    if (result.footnotes.length > 0) {
      console.log('Footnotes:');
      result.footnotes.forEach((footnote, index) => {
        console.log(`\nFootnote ${index + 1}:`);
        console.log(footnote);
      });
    }
    
    console.log(`\nEndnotes count: ${result.endnotes.length}\n`);
    
    if (result.endnotes.length > 0) {
      console.log('Endnotes:');
      result.endnotes.forEach((endnote, index) => {
        console.log(`\nEndnote ${index + 1}:`);
        console.log(endnote);
      });
    }
    
    console.log('\n========================================');
    console.log('Done!');
    console.log('========================================');
  } catch (err) {
    console.error('Extraction failed:', err.message);
    process.exit(1);
  }
}

if (require.main === module) {
  cli();
}

module.exports = { extractFootnotes };
