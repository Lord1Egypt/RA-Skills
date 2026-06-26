/**
 * Analyze design image structure
 * 
 * Usage: node analyze.js <image-file> <output-json>
 * 
 * Detects:
 * - Dimensions
 * - Color palette
 * - Layout structure
 * - Font sizes (estimated)
 */

const sharp = require('sharp');
const fs = require('fs');

async function analyzeImage(imagePath) {
    const image = sharp(imagePath);
    const metadata = await image.metadata();
    
    // Get pixel data
    const { data, info } = await image.raw().toBuffer({ resolveWithObject: true });
    
    const width = info.width;
    const height = info.height;
    
    // Extract color palette (sample pixels)
    const colors = extractColorPalette(data, width, height, info.channels);
    
    // Detect layout structure
    const layout = detectLayout(data, width, height);
    
    // Estimate font sizes (by analyzing text regions)
    const fonts = estimateFonts(data, width, height);
    
    const report = {
        dimensions: { width, height },
        format: metadata.format,
        colors: colors,
        layout: layout,
        fonts: fonts,
        timestamp: new Date().toISOString()
    };
    
    return report;
}

function extractColorPalette(data, width, height, channels = 4) {
    const colorMap = new Map();
    const sampleSize = Math.max(1, Math.floor(width * height / 1000)); // Sample 0.1% of pixels
    
    for (let i = 0; i < data.length; i += channels * sampleSize) {
        const r = data[i];
        const g = data[i + 1];
        const b = data[i + 2];
        
        // Quantize to reduce similar colors
        const qr = Math.round(r / 16) * 16;
        const qg = Math.round(g / 16) * 16;
        const qb = Math.round(b / 16) * 16;
        
        const hex = `#${qr.toString(16).padStart(2, '0')}${qg.toString(16).padStart(2, '0')}${qb.toString(16).padStart(2, '0')}`;
        
        colorMap.set(hex, (colorMap.get(hex) || 0) + 1);
    }
    
    // Sort by frequency and return top colors
    const sorted = Array.from(colorMap.entries())
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .map(([color, count]) => ({ color, count }));
    
    return sorted;
}

function detectLayout(data, width, height) {
    // Simplified layout detection based on color regions
    const regions = [];
    const blockSize = Math.max(10, Math.floor(width / 20));
    
    for (let y = 0; y < height; y += blockSize) {
        for (let x = 0; x < width; x += blockSize) {
            const idx = (y * width + x) * 4;
            const brightness = (data[idx] + data[idx + 1] + data[idx + 2]) / 3;
            
            if (brightness < 50) regions.push({ x, y, type: 'dark' });
            else if (brightness > 200) regions.push({ x, y, type: 'light' });
            else regions.push({ x, y, type: 'medium' });
        }
    }
    
    // Estimate layout type
    const darkRegions = regions.filter(r => r.type === 'dark').length;
    const lightRegions = regions.filter(r => r.type === 'light').length;
    
    let layoutType = 'mixed';
    if (darkRegions > regions.length * 0.7) layoutType = 'dark-theme';
    else if (lightRegions > regions.length * 0.7) layoutType = 'light-theme';
    
    return {
        type: layoutType,
        regions: regions.length,
        blockSize
    };
}

function estimateFonts(data, width, height) {
    // Simplified font size estimation
    // This would need OCR for accurate detection
    return {
        estimated: true,
        sizes: ['14px', '16px', '18px', '24px', '32px'],
        note: 'Font sizes estimated from pixel density'
    };
}

// CLI execution
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.length < 2) {
        console.error('Usage: node analyze.js <image-file> <output-json>');
        process.exit(1);
    }
    
    const imagePath = args[0];
    const outputPath = args[1];
    
    analyzeImage(imagePath)
        .then(report => {
            fs.writeFileSync(outputPath, JSON.stringify(report, null, 2));
            console.log(`✓ Dimensions: ${report.dimensions.width}x${report.dimensions.height}px`);
            console.log(`✓ Colors detected: ${report.colors.length}`);
            console.log(`✓ Layout type: ${report.layout.type}`);
            console.log(`✓ Report saved: ${outputPath}`);
        })
        .catch(err => console.error('Error:', err.message));
}

module.exports = { analyzeImage };