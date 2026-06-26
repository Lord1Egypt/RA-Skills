/**
 * Pixel-level comparison using pixelmatch
 * 
 * Usage: node compare.js <original-image> <rendered-image> <diff-output> [--threshold 0.1]
 * 
 * Outputs:
 * - diff image (visual differences)
 * - JSON report with metrics
 */

const pixelmatch = require('pixelmatch');
const { PNG } = require('pngjs');
const fs = require('fs');
const path = require('path');

function compareImages(originalPath, renderedPath, diffPath, threshold = 0.1) {
    // Read images
    const originalImg = fs.readFileSync(originalPath);
    const renderedImg = fs.readFileSync(renderedPath);
    
    const original = PNG.sync.read(originalImg);
    const rendered = PNG.sync.read(renderedImg);
    
    // Check dimensions
    if (original.width !== rendered.width || original.height !== rendered.height) {
        const report = {
            matchScore: 0,
            diffPixels: 0,
            totalPixels: 0,
            error: 'Dimensions mismatch',
            originalDimensions: { width: original.width, height: original.height },
            renderedDimensions: { width: rendered.width, height: rendered.height }
        };
        
        fs.writeFileSync(diffPath + '.json', JSON.stringify(report, null, 2));
        return report;
    }
    
    const width = original.width;
    const height = original.height;
    
    // Create diff image
    const diff = new PNG({ width, height });
    
    // Compare pixel by pixel
    const numDiffPixels = pixelmatch(
        original.data,
        rendered.data,
        diff.data,
        width,
        height,
        { threshold }
    );
    
    // Calculate match score
    const totalPixels = width * height;
    const matchScore = ((totalPixels - numDiffPixels) / totalPixels) * 100;
    
    // Save diff image
    fs.writeFileSync(diffPath, PNG.sync.write(diff));
    
    // Generate report
    const report = {
        matchScore: parseFloat(matchScore.toFixed(2)),
        diffPixels: numDiffPixels,
        totalPixels,
        threshold,
        dimensions: { width, height },
        timestamp: new Date().toISOString()
    };
    
    fs.writeFileSync(diffPath + '.json', JSON.stringify(report, null, 2));
    
    return report;
}

// CLI execution
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.length < 3) {
        console.error('Usage: node compare.js <original-image> <rendered-image> <diff-output> [--threshold 0.1]');
        process.exit(1);
    }
    
    const originalPath = args[0];
    const renderedPath = args[1];
    const diffPath = args[2];
    let threshold = 0.1;
    
    // Parse optional threshold
    if (args[3] === '--threshold' && args[4]) {
        threshold = parseFloat(args[4]);
    }
    
    const report = compareImages(originalPath, renderedPath, diffPath, threshold);
    
    console.log(`✓ Match score: ${report.matchScore}%`);
    console.log(`✓ Diff pixels: ${report.diffPixels} / ${report.totalPixels}`);
    console.log(`✓ Diff image: ${diffPath}`);
    console.log(`✓ Report: ${diffPath}.json`);
}

module.exports = { compareImages };