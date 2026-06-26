#!/usr/bin/env node
/**
 * Export HTML reports to PNG/JPEG image using Playwright
 * Captures the full page or specific viewport
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function exportImage() {
    const args = process.argv.slice(2);
    let htmlPath = 'data/reports/html/index.html';
    let outputPath = null;
    let format = 'png'; // png or jpeg
    let fullPage = false;

    for (let i = 0; i < args.length; i++) {
        if (args[i] === '-o' && args[i + 1]) {
            outputPath = args[i + 1];
            i++;
        } else if (args[i] === '--jpeg' || args[i] === '-j') {
            format = 'jpeg';
        } else if (args[i] === '--full' || args[i] === '-f') {
            fullPage = true;
        } else if (!args[i].startsWith('-')) {
            htmlPath = args[i];
        }
    }

    const resolvedHtml = path.resolve(htmlPath);
    const htmlFile = path.basename(resolvedHtml, '.html');
    const date = new Date().toISOString().split('T')[0];
    const imgDir = path.join(path.dirname(resolvedHtml), '..', 'images', date);
    const ext = format === 'jpeg' ? 'jpg' : 'png';
    const defaultOutput = path.join(imgDir, `${htmlFile}-${date}.${ext}`);
    const resolvedOutput = outputPath || defaultOutput;

    fs.mkdirSync(path.dirname(resolvedOutput), { recursive: true });

    console.log(`Exporting: ${resolvedHtml}`);
    console.log(`Output: ${resolvedOutput}`);

    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    // Set viewport for best chart rendering
    await page.setViewportSize({ width: 1400, height: 900 });
    await page.goto(`file://${resolvedHtml}`, { waitUntil: 'networkidle' });

    // Wait for ECharts to fully render
    await page.waitForTimeout(3000);

    // Check if ECharts rendered
    const chartCount = await page.evaluate(() => {
        return document.querySelectorAll('[_echarts_instance_]').length;
    });
    console.log(`ECharts instances found: ${chartCount}`);

    const screenshotOptions = {
        type: format,
        fullPage: fullPage,
        omitBackground: false
    };

    if (format === 'jpeg') {
        screenshotOptions.quality = 90;
    }

    await page.screenshot(screenshotOptions);

    const screenshot = await page.screenshot(screenshotOptions);
    fs.writeFileSync(resolvedOutput, screenshot);

    await browser.close();

    const stats = fs.statSync(resolvedOutput);
    const sizeKb = (stats.size / 1024).toFixed(1);

    console.log(`\n✅ Image exported successfully!`);
    console.log(`   Path: ${resolvedOutput}`);
    console.log(`   Size: ${sizeKb} KB`);
    console.log(`   Format: ${format.toUpperCase()}`);
    if (fullPage) {
        console.log(`   Mode: Full page`);
    } else {
        console.log(`   Mode: Viewport (${page.viewportSize().width}x${page.viewportSize().height})`);
    }
}

exportImage().catch(err => {
    console.error(`❌ Export failed: ${err.message}`);
    process.exit(1);
});
