/**
 * path-mapper.js - Windows/WSL path conversion
 */

function toWslPath(winPath) {
  if (!winPath) return null;
  let p = winPath.replace(/\\/g, '/');
  if (p.match(/^[A-Za-z]:/)) {
    const drive = p[0].toLowerCase();
    p = '/mnt/' + drive + p.slice(2);
  }
  return p;
}

function toWindowsPath(wslPath) {
  if (!wslPath) return null;
  if (wslPath.startsWith('/mnt/')) {
    const parts = wslPath.split('/');
    if (parts.length >= 3 && parts[2].length === 1) {
      const drive = parts[2].toUpperCase();
      const rest = parts.slice(3).join('/');
      return drive + ':\\' + rest.replace(/\//g, '\\');
    }
  }
  return wslPath.replace(/\//g, '\\');
}

function test() {
  const cases = [
    'C:\\Users\\Admin\\.openclaw\\workspace\\output\\test.xlsx',
    '/mnt/c/Users/Admin/.openclaw/workspace/output/test.xlsx'
  ];
  for (const c of cases) {
    console.log('Input:', c);
    console.log('  -> WSL:', toWslPath(c));
    console.log('  -> Win:', toWindowsPath(c));
  }
}

if (require.main === module) {
  test();
}

module.exports = { toWslPath, toWindowsPath };
