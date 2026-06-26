#!/usr/bin/env node
/**
 * Export HTML reports to PDF using Playwright via npx
 * Waits for ECharts to fully render before PDF export
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function exportPDF() {
    const args = process.argv.slice(2);
    let htmlPath = 'data/reports/html/index.html';
    let outputPath = null;

    for (let i = 0; i < args.length; i++) {
        if (args[i] === '-o' && args[i + 1]) {
            outputPath = args[i + 1];
            i++;
        } else if (!args[i].startsWith('-')) {
            htmlPath = args[i];
        }
    }

    const resolvedHtml = path.resolve(htmlPath);
    const htmlFile = path.basename(resolvedHtml, '.html');
    const date = new Date().toISOString().split('T')[0];
    const pdfDir = path.join(path.dirname(resolvedHtml), '..', 'pdf', date);
    const defaultOutput = path.join(pdfDir, `${htmlFile}-${date}.pdf`);
    const resolvedOutput = outputPath || defaultOutput;

    fs.mkdirSync(path.dirname(resolvedOutput), { recursive: true });

    console.log(`Exporting: ${resolvedHtml}`);
    console.log(`Output: ${resolvedOutput}`);

    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    await page.setViewportSize({ width: 1400, height: 1000 });
    await page.goto(`file://${resolvedHtml}`, { waitUntil: 'networkidle' });

    // Wait for ECharts to fully render
    await page.waitForTimeout(3000);

    // Check if ECharts rendered
    const chartCount = await page.evaluate(() => {
        return document.querySelectorAll('[_echarts_instance_]').length;
    });
    console.log(`ECharts instances found: ${chartCount}`);

    await page.pdf({
        path: resolvedOutput,
        format: 'A4',
        printBackground: true,
        margin: { top: '15mm', bottom: '15mm', left: '15mm', right: '15mm' },
        displayHeaderFooter: true,
        headerTemplate: '<div></div>',
        footerTemplate: `
            <div style="width: 100%; font-size: 10px; text-align: center; color: #666;">
                Page <span class="pageNumber"></span> of <span class="totalPages"></span>
                | competitive-ops v2 | ${date}
            </div>
        `
    });

    await browser.close();

    const stats = fs.statSync(resolvedOutput);
    const sizeKb = (stats.size / 1024).toFixed(1);

    console.log(`\n✅ PDF exported successfully!`);
    console.log(`   Path: ${resolvedOutput}`);
    console.log(`   Size: ${sizeKb} KB`);
}

exportPDF().catch(err => {
    console.error(`❌ Export failed: ${err.message}`);
    process.exit(1);
});
