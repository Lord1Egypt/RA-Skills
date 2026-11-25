// Use an already installed Playwright (no runtime dependency or auto-install).
const assert=require('assert/strict');
const path=require('path');
const {chromium}=require(process.env.DESKTOP_PILOT_PLAYWRIGHT || 'playwright');
(async()=>{
 const browser=await chromium.launch({headless:true});
 try {
  const page=await browser.newPage();
  await page.goto('about:blank');
  await page.addScriptTag({path:path.join(__dirname,'../scripts/browser/overlay.js')});
  await page.evaluate(()=>window.__dpOverlay.show('Test status'));
  assert.equal(await page.locator('[data-desktop-pilot-overlay] .txt').textContent(),'Test status');
  assert.equal(await page.locator('[data-desktop-pilot-overlay] button').count(),0);
  assert.equal(await page.evaluate(()=>typeof window.__dpOverlay.stopped),'undefined');
  await page.evaluate(()=>window.__dpOverlay.text('<img src=x onerror=alert(1)>'));
  assert.equal(await page.locator('[data-desktop-pilot-overlay] img').count(),0);
  await page.evaluate(()=>window.__dpOverlay.hide());
  assert.equal(await page.locator('[data-desktop-pilot-overlay]').count(),0);
  await page.evaluate(()=>window.__dpOverlay.show('Watchdog',{idleMs:50}));
  await page.waitForFunction(()=>!window.__dpOverlay.visible());
  console.log('PASS: real Chromium status rendering, no page cancellation, text escaping, hide, idle watchdog');
 } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});
