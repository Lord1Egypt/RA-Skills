/**
 * ClickBank Product Scraper - MVP
 * Scrapes top Health & Fitness products from CBTrends.com
 */

const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  affiliateId: process.env.CB_AFFILIATE_ID || 'YOUR_CB_NICKNAME',
  sources: [
    {
      name: 'Health & Fitness (by gravity)',
      url: 'https://www.cbtrends.com/browse-clickbank-marketplace/-1/94/Health%2B%2526%2BFitness/1/gravity/',
      category: 'Health & Fitness',
    },
  ],
  outputDir: path.join(__dirname, 'output'),
  userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0',
};

function makeHoplink(vendorId, affiliateId) {
  return `https://hop.clickbank.net/?affiliate=${affiliateId}&vendor=${vendorId}`;
}

function estimateMonthlySales(gravity) {
  if (gravity > 500) return '50,000+';
  if (gravity > 200) return '10,000-50,000';
  if (gravity > 100) return '5,000-10,000';
  if (gravity > 50) return '1,000-5,000';
  if (gravity > 20) return '500-1,000';
  return '100-500';
}

async function fetchPage(url) {
  const res = await fetch(url, {
    headers: { 'User-Agent': CONFIG.userAgent, 'Accept': 'text/html' }
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.text();
}

function parseCBTrends(html, category) {
  const $ = cheerio.load(html);
  const products = [];

  // Extract product names from get-product links (every other one is a duplicate)
  const productNames = [];
  const productIds = [];
  $('a[href*="get-product"]').each((i, el) => {
    const text = $(el).text().trim();
    if (text.length > 2) {
      productNames.push(text);
      // Get the product ID from href
      const href = $(el).attr('href') || '';
      const idMatch = href.match(/productid=([a-f0-9]+)/);
      if (idMatch) productIds.push(idMatch[1]);
    }
  });

  // Extract vendor IDs from clickbank-product links in the product area
  const vendorIds = [];
  $('a[href*="clickbank-product/"]').each((i, el) => {
    const href = $(el).attr('href') || '';
    const vMatch = href.match(/clickbank-product\/([^.]+)/);
    if (vMatch) vendorIds.push(vMatch[1]);
  });

  // Extract stats from body text
  const bodyText = $('body').text();
  const statRegex = /¤\s*Popularity:\s*(\d+)\s*¤\s*Gravity:\s*([\d.]+)\s*¤\s*\$\/Sale:\s*([\d.]+)\s*¤\s*%\/Sale:\s*([\d.]+)\s*¤\s*Commission:\s*([\d.]+)\s*¤\s*Referred:\s*([\d.]+)\s*¤\s*%\/Rebill:\s*([\d.]+)\s*¤\s*Rebill Amt:\s*([\d.]+)\s*¤/g;

  const stats = [];
  let match;
  while ((match = statRegex.exec(bodyText)) !== null) {
    stats.push({
      popularityRank: parseInt(match[1]),
      gravity: parseFloat(match[2]),
      avgSaleAmount: parseFloat(match[3]),
      salePct: parseFloat(match[4]),
      commissionPct: parseInt(match[5]),
      referredPct: parseFloat(match[6]),
      rebillPct: parseFloat(match[7]),
      rebillAmount: parseFloat(match[8]),
    });
  }

  // Combine: names[i] + stats[i] + vendorIds[i]
  const count = Math.min(productNames.length, stats.length);
  for (let i = 0; i < count; i++) {
    const s = stats[i];
    const vendorId = vendorIds[i] || null;
    products.push({
      name: productNames[i],
      vendorId,
      category,
      gravity: s.gravity,
      popularityRank: s.popularityRank,
      avgSaleAmount: s.avgSaleAmount,
      salePct: s.salePct,
      commissionPct: s.commissionPct,
      referredPct: s.referredPct,
      rebillPct: s.rebillPct,
      rebillAmount: s.rebillAmount,
      estimatedMonthlySales: estimateMonthlySales(s.gravity),
      hoplink: vendorId ? makeHoplink(vendorId, CONFIG.affiliateId) : null,
      source: 'cbtrends',
      scrapedAt: new Date().toISOString(),
    });
  }

  return products;
}

async function main() {
  console.log('╔══════════════════════════════════════════════╗');
  console.log('║  ClickBank Product Scraper - Health/Fitness  ║');
  console.log('╚══════════════════════════════════════════════╝\n');

  if (!fs.existsSync(CONFIG.outputDir)) fs.mkdirSync(CONFIG.outputDir, { recursive: true });

  let allProducts = [];
  for (const source of CONFIG.sources) {
    try {
      console.log(`[Scraper] Fetching: ${source.name}`);
      const html = await fetchPage(source.url);
      const products = parseCBTrends(html, source.category);
      console.log(`[Scraper] Parsed ${products.length} products`);
      allProducts.push(...products);
    } catch (err) {
      console.error(`[Error] ${source.name}: ${err.message}`);
    }
  }

  allProducts.sort((a, b) => b.gravity - a.gravity);
  const top10 = allProducts.slice(0, 10);

  console.log(`\n📊 Results: ${allProducts.length} total, top 10:\n`);
  top10.forEach((p, i) => {
    console.log(`  ${String(i + 1).padStart(2)}. ${p.name}`);
    console.log(`      Gravity: ${p.gravity} | Commission: ${p.commissionPct}% | Avg Sale: $${p.avgSaleAmount}`);
    console.log(`      Est. Sales: ${p.estimatedMonthlySales} | Vendor: ${p.vendorId || 'unknown'}`);
    if (p.hoplink) console.log(`      Hoplink: ${p.hoplink}`);
    console.log();
  });

  const ts = new Date().toISOString().split('T')[0];
  fs.writeFileSync(path.join(CONFIG.outputDir, `products-${ts}.json`), JSON.stringify(allProducts, null, 2));
  fs.writeFileSync(path.join(CONFIG.outputDir, `top10-${ts}.json`), JSON.stringify(top10, null, 2));
  fs.writeFileSync(path.join(CONFIG.outputDir, 'latest.json'), JSON.stringify({
    scrapedAt: new Date().toISOString(), totalProducts: allProducts.length, top10, allProducts
  }, null, 2));

  console.log(`💾 Saved ${allProducts.length} products to ${CONFIG.outputDir}`);
  return { top10, allProducts };
}

if (require.main === module) main().catch(err => { console.error('Fatal:', err); process.exit(1); });
module.exports = { main, parseCBTrends, makeHoplink, CONFIG };
