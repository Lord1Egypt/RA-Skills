const mammoth = require("mammoth");
const fs = require("fs/promises");

async function convertDocxToHtml(inputPath, outputPath) {
    try {
        const buffer = await fs.readFile(inputPath);
        const result = await mammoth.convertToHtml({ buffer: buffer });
        await fs.writeFile(outputPath, result.value);
        console.log(`Successfully converted ${inputPath} to ${outputPath}`);
    } catch (error) {
        console.error(`Error converting DOCX to HTML: ${error.message}`);
        process.exit(1);
    }
}

const args = process.argv.slice(2);
if (args.length < 2) {
    console.error("Usage: node docx-converter.js <input_path> <output_path>");
    process.exit(1);
}

const inputPath = args[0];
const outputPath = args[1];

convertDocxToHtml(inputPath, outputPath);
