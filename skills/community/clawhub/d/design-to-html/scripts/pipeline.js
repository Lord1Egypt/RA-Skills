/**
 * Main pipeline - Iterative design-to-HTML conversion
 * 
 * Usage: node pipeline.js <original-image> [--threshold 95] [--iterations 5] [--output-dir ./output]
 * 
 * Process:
 * 1. Analyze design → Generate initial HTML
 * 2. Render → Compare → Optimize (loop)
 * 3. Output final HTML + comparison report
 */

const fs = require('fs');
const path = require('path');
const { analyzeImage } = require('./analyze.js');
const { renderHtmlToImage } = require('./render.js');
const { compareImages } = require('./compare.js');

async function runPipeline(originalImage, options = {}) {
    const {
        threshold = 95,
        maxIterations = 5,
        outputDir = './output',
        width = null,
        height = null
    } = options;
    
    // Create output directory
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }
    
    console.log('\n=== Design-to-HTML Pipeline ===\n');
    console.log(`Input: ${originalImage}`);
    console.log(`Threshold: ${threshold}%`);
    console.log(`Max iterations: ${maxIterations}`);
    console.log(`Output: ${outputDir}\n`);
    
    // Step 1: Analyze design
    console.log('[Step 1] Analyzing design...');
    const analysisReport = await analyzeImage(originalImage);
    const dimensions = analysisReport.dimensions;
    
    fs.writeFileSync(
        path.join(outputDir, 'analysis.json'),
        JSON.stringify(analysisReport, null, 2)
    );
    
    console.log(`✓ Dimensions: ${dimensions.width}x${dimensions.height}px`);
    console.log(`✓ Colors: ${analysisReport.colors.length} detected`);
    console.log(`✓ Layout: ${analysisReport.layout.type}\n`);
    
    // Step 2: Generate initial HTML (placeholder - model will generate)
    const initialHtml = generatePlaceholderHtml(analysisReport);
    const initialHtmlPath = path.join(outputDir, 'iteration_1.html');
    fs.writeFileSync(initialHtmlPath, initialHtml);
    
    console.log('[Step 2] Generated initial HTML placeholder');
    console.log(`✓ Saved: ${initialHtmlPath}`);
    console.log('✓ Next: Model will refine this HTML based on analysis\n');
    
    // Step 3-4: Iteration loop
    const iterations = [];
    
    for (let i = 1; i <= maxIterations; i++) {
        console.log(`\n[Iteration ${i}/${maxIterations}]`);
        
        const htmlPath = path.join(outputDir, `iteration_${i}.html`);
        const renderedPath = path.join(outputDir, `rendered_${i}.png`);
        const diffPath = path.join(outputDir, `diff_${i}.png`);
        
        // Check if HTML exists
        if (!fs.existsSync(htmlPath)) {
            console.log(`⚠ No HTML file for iteration ${i}, skipping...`);
            continue;
        }
        
        // Render HTML
        console.log(`Rendering HTML...`);
        await renderHtmlToImage(htmlPath, renderedPath, dimensions.width, dimensions.height);
        console.log(`✓ Rendered: ${renderedPath}`);
        
        // Compare
        console.log(`Comparing with original...`);
        const report = compareImages(originalImage, renderedPath, diffPath);
        console.log(`✓ Match score: ${report.matchScore}%`);
        
        iterations.push({
            iteration: i,
            matchScore: report.matchScore,
            htmlPath,
            renderedPath,
            diffPath,
            report
        });
        
        // Check if threshold reached
        if (report.matchScore >= threshold) {
            console.log(`\n✅ Threshold reached (${report.matchScore}% >= ${threshold}%)`);
            break;
        }
        
        // Generate next HTML placeholder for model
        if (i < maxIterations) {
            const nextHtmlPath = path.join(outputDir, `iteration_${i+1}.html`);
            // Copy current HTML as base for next iteration
            // Model will refine based on diff report
            fs.writeFileSync(nextHtmlPath, fs.readFileSync(htmlPath));
            console.log(`✓ Created placeholder for iteration ${i+1}`);
        }
    }
    
    // Step 5: Generate final report
    console.log('\n[Finalizing]');
    const finalReport = generateFinalReport(iterations, threshold);
    fs.writeFileSync(
        path.join(outputDir, 'comparison_report.md'),
        finalReport
    );
    
    // Find best iteration
    const best = iterations.sort((a, b) => b.matchScore - a.matchScore)[0];
    if (best) {
        fs.writeFileSync(
            path.join(outputDir, 'final.html'),
            fs.readFileSync(best.htmlPath)
        );
        console.log(`✓ Best match: Iteration ${best.iteration} (${best.matchScore}%)`);
        console.log(`✓ Final HTML: final.html`);
    }
    
    console.log(`✓ Report: comparison_report.md`);
    console.log('\n=== Pipeline Complete ===\n');
    
    return {
        iterations,
        bestIteration: best,
        finalReport,
        outputDir
    };
}

function generatePlaceholderHtml(analysis) {
    const { dimensions, colors, layout } = analysis;
    
    // Generate basic HTML structure based on analysis
    const primaryColor = colors[0]?.color || '#FFFFFF';
    
    return `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Design Mockup</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            width: ${dimensions.width}px;
            height: ${dimensions.height}px;
            background: ${primaryColor};
            font-family: Arial, sans-serif;
        }
        
        /* TODO: Model will fill in actual design details */
        /* Based on analysis: ${layout.type} layout */
        /* Primary colors: ${colors.slice(0, 3).map(c => c.color).join(', ')} */
    </style>
</head>
<body>
    <!-- TODO: Model will generate actual content -->
    <div style="width: ${dimensions.width}px; height: ${dimensions.height}px;">
        <!-- Placeholder: Model will analyze design image and generate matching HTML -->
    </div>
</body>
</html>`;
}

function generateFinalReport(iterations, threshold) {
    const lines = [
        '# Design-to-HTML Comparison Report',
        '',
        `**Target threshold**: ${threshold}%`,
        `**Iterations**: ${iterations.length}`,
        '',
        '## Iteration History',
        ''
    ];
    
    for (const iter of iterations) {
        lines.push(`### Iteration ${iter.iteration}`);
        lines.push(`- **Match score**: ${iter.matchScore}%`);
        lines.push(`- **Diff pixels**: ${iter.report.diffPixels}`);
        lines.push(`- **HTML**: ${iter.htmlPath}`);
        lines.push(`- **Rendered**: ${iter.renderedPath}`);
        lines.push(`- **Diff image**: ${iter.diffPath}`);
        lines.push('');
    }
    
    const best = iterations.sort((a, b) => b.matchScore - a.matchScore)[0];
    if (best) {
        lines.push('## Best Result');
        lines.push(`- **Iteration**: ${best.iteration}`);
        lines.push(`- **Match score**: ${best.matchScore}%`);
        lines.push(`- **Status**: ${best.matchScore >= threshold ? '✅ Threshold reached' : '⚠ Below threshold'}`);
    }
    
    return lines.join('\n');
}

// CLI execution
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.length < 1) {
        console.error('Usage: node pipeline.js <original-image> [--threshold 95] [--iterations 5] [--output-dir ./output]');
        process.exit(1);
    }
    
    const originalImage = args[0];
    const options = {
        threshold: 95,
        maxIterations: 5,
        outputDir: './output'
    };
    
    // Parse options
    for (let i = 1; i < args.length; i++) {
        if (args[i] === '--threshold' && args[i+1]) {
            options.threshold = parseInt(args[i+1]);
            i++;
        } else if (args[i] === '--iterations' && args[i+1]) {
            options.maxIterations = parseInt(args[i+1]);
            i++;
        } else if (args[i] === '--output-dir' && args[i+1]) {
            options.outputDir = args[i+1];
            i++;
        }
    }
    
    runPipeline(originalImage, options)
        .catch(err => console.error('Pipeline error:', err.message));
}

module.exports = { runPipeline };