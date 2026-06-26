/**
 * Render HTML to PNG screenshot using Puppeteer
 * 
 * Usage: node render.js <html-file> <output-image> [--width W] [--height H]
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function renderHtmlToImage(htmlFile, outputImage, width = 1920, height = 1080) {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    // Set viewport
    await page.setViewport({ width, height });
    
    // Load HTML file
    const htmlContent = fs.readFileSync(htmlFile, 'utf8');
    await page.setContent(htmlContent, { waitUntil: 'networkidle0' });
    
    // Take screenshot
    await page.screenshot({
        path: outputImage,
        type: 'png',
        fullPage: false
    });
    
    await browser.close();
    
    return outputImage;
}

// CLI execution
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.length < 2) {
        console.error('Usage: node render.js <html-file> <output-image> [--width W] [--height H]');
        process.exit(1);
    }
    
    const htmlFile = args[0];
    const outputImage = args[1];
    
    // Parse optional dimensions
    let width = 1920;
    let height = 1080;
    
    for (let i = 2; i < args.length; i++) {
        if (args[i] === '--width' && args[i+1]) {
            width = parseInt(args[i+1]);
            i++;
        } else if (args[i] === '--height' && args[i+1]) {
            height = parseInt(args[i+1]);
            i++;
        }
    }
    
    renderHtmlToImage(htmlFile, outputImage, width, height)
        .then(() => console.log(`✓ Rendered: ${outputImage}`))
        .catch(err => console.error('Error:', err.message));
}

module.exports = { renderHtmlToImage };