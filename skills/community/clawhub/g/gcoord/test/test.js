const { describe, it } = require('node:test');
const assert = require('node:assert');
const { execSync } = require('child_process');
const path = require('path');

const CLI = path.join(__dirname, '..', 'index.js');

function run(args) {
  return execSync(`node "${CLI}" ${args}`, { encoding: 'utf-8' });
}

function runErr(args) {
  try {
    execSync(`node "${CLI}" ${args}`, { encoding: 'utf-8', stdio: 'pipe' });
    return null;
  } catch (e) {
    return e.stderr || e.message;
  }
}

describe('单点坐标转换', () => {
  it('WGS84 → GCJ02', () => {
    const out = run('--input "116.403988,39.914266" --from WGS84 --to GCJ02');
    assert.match(out, /转换: WGS84 → GCJ02/);
    assert.match(out, /结果:/);
    // 转换后经度应在 116.4 附近
    const nums = out.match(/结果:\s*([\d.]+),\s*([\d.]+)/);
    assert.ok(nums, '应输出坐标数值');
    const lng = parseFloat(nums[1]);
    assert.ok(lng > 116 && lng < 117, '经度应在合理范围');
  });

  it('WGS84 → BD09', () => {
    const out = run('--input "116.403988,39.914266" --from WGS84 --to BD09');
    assert.match(out, /转换: WGS84 → BD09/);
  });

  it('GCJ02 → WGS84', () => {
    const out = run('--input "116.410000,39.920000" --from GCJ02 --to WGS84');
    assert.match(out, /转换: GCJ02 → WGS84/);
  });
});

describe('数组格式转换', () => {
  it('[lng, lat] 格式', () => {
    const out = run('--input "[116.403988,39.914266]" --from WGS84 --to GCJ02');
    assert.match(out, /结果:/);
  });
});
describe('批量坐标转换 (Bug 1 修复验证)', () => {
  it('多行坐标批量转换', () => {
    const input = '116.403988,39.914266\n121.499763,31.239586';
    const out = run(`--input "${input}" --from WGS84 --to GCJ02`);
    assert.match(out, /转换: WGS84 → GCJ02/);
    // 批量结果应包含两行坐标
    const resultLine = out.split('\n').find(l => l.startsWith('结果:'));
    assert.ok(resultLine, '应有结果输出');
  });
});

describe('GeoJSON 格式转换', () => {
  it('Point GeoJSON', () => {
    const geojson = JSON.stringify({
      type: 'Point',
      coordinates: [116.403988, 39.914266]
    });
    const out = run(`--input '${geojson}' --from WGS84 --to GCJ02`);
    assert.match(out, /转换: WGS84 → GCJ02/);
    assert.match(out, /结果:/);
  });
});

describe('无效坐标系报错 (Bug 2 修复验证)', () => {
  it('无效 from 坐标系应给出友好提示', () => {
    const err = runErr('--input "116.403988,39.914266" --from INVALID --to GCJ02');
    assert.ok(err, '应报错');
    assert.match(err, /不支持的坐标系/);
  });

  it('无效 to 坐标系应给出友好提示', () => {
    const err = runErr('--input "116.403988,39.914266" --from WGS84 --to FAKE');
    assert.ok(err, '应报错');
    assert.match(err, /不支持的坐标系/);
  });
});

describe('中英文别名解析', () => {
  it('百度 → BD09', () => {
    const out = run('--input "116.403988,39.914266" --from WGS84 --to 百度');
    assert.match(out, /转换: WGS84 → BD09/);
  });

  it('高德 → GCJ02', () => {
    const out = run('--input "116.403988,39.914266" --from WGS84 --to 高德');
    assert.match(out, /转换: WGS84 → GCJ02/);
  });

  it('gps → WGS84', () => {
    const out = run('--input "116.410000,39.920000" --from gps --to GCJ02');
    assert.match(out, /转换: WGS84 → GCJ02/);
  });

  it('amap → GCJ02', () => {
    const out = run('--input "116.403988,39.914266" --from WGS84 --to amap');
    assert.match(out, /转换: WGS84 → GCJ02/);
  });
});

describe('空输入 / 无效输入', () => {
  it('空输入应报错', () => {
    const err = runErr('--input "" --from WGS84 --to GCJ02');
    assert.ok(err, '空输入应报错');
  });

  it('无效输入应报错', () => {
    const err = runErr('--input "abc" --from WGS84 --to GCJ02');
    assert.ok(err, '无效输入应报错');
  });
});

describe('边界情况', () => {
  it('空格分隔坐标', () => {
    const out = run('--input "116.403988 39.914266" --from WGS84 --to GCJ02');
    assert.match(out, /结果:/);
  });

  it('默认坐标系 (WGS84 → GCJ02)', () => {
    const out = run('--input "116.403988,39.914266"');
    assert.match(out, /转换: WGS84 → GCJ02/);
  });
});
