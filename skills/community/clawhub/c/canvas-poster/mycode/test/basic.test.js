const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { buildPoster, sectionHeight, drawSection } = require('../lib/builder');
const { createCanvas } = require('../lib/core');

function tmpFile() {
  return path.join(os.tmpdir(), `canvas-poster-test-${Date.now()}-${Math.random().toString(36).slice(2)}.png`);
}

function posterWith(sections) {
  return buildPoster({ width: 800, sections });
}

// ===== Each section type renders without error =====

describe('section rendering', () => {
  it('kpi-cards', () => {
    const { canvas } = posterWith([{
      type: 'kpi-cards',
      cards: [
        { label: 'A', value: '100' },
        { label: 'B', value: '200', color: 'red' },
        { label: 'C', value: '300', color: 'green', sub: 'note' },
      ],
    }]);
    assert.ok(canvas.width === 800);
    assert.ok(canvas.height > 0);
  });

  it('bar-chart', () => {
    const { canvas } = posterWith([{
      type: 'bar-chart',
      title: 'Test Bars',
      bars: [
        { name: 'X', value: 100 },
        { name: 'Y', value: 200, pct: 66.7 },
      ],
    }]);
    assert.ok(canvas.height > 0);
  });

  it('pie-chart', () => {
    const { canvas } = posterWith([{
      type: 'pie-chart',
      slices: [
        { name: 'A', value: 30 },
        { name: 'B', value: 70 },
      ],
    }]);
    assert.ok(canvas.height > 0);
  });

  it('pie-chart with many slices', () => {
    const slices = Array.from({ length: 10 }, (_, i) => ({ name: `Item ${i}`, value: 10 + i }));
    const { canvas } = posterWith([{ type: 'pie-chart', slices }]);
    assert.ok(canvas.height > 0);
  });

  it('table', () => {
    const { canvas } = posterWith([{
      type: 'table',
      headers: ['Name', 'Value'],
      rows: [['A', '1'], ['B', '2']],
    }]);
    assert.ok(canvas.height > 0);
  });

  it('tips', () => {
    const { canvas } = posterWith([{
      type: 'tips',
      items: ['Tip 1', 'Tip 2', 'Tip 3'],
    }]);
    assert.ok(canvas.height > 0);
  });

  it('divider', () => {
    const { canvas } = posterWith([{ type: 'divider' }]);
    assert.ok(canvas.height > 0);
  });

  it('line-chart', () => {
    const { canvas } = posterWith([{
      type: 'line-chart',
      title: 'Test Lines',
      xLabels: ['Jan', 'Feb', 'Mar'],
      lines: [
        { name: 'A', data: [10, 20, 15], color: '#3b82f6' },
        { name: 'B', data: [5, 18, 25] },
      ],
    }]);
    assert.ok(canvas.height > 0);
  });

  it('line-chart single line no legend', () => {
    const { canvas } = posterWith([{
      type: 'line-chart',
      lines: [{ name: 'Solo', data: [1, 2, 3, 4] }],
    }]);
    assert.ok(canvas.height > 0);
  });

  it('area-chart', () => {
    const { canvas } = posterWith([{
      type: 'area-chart',
      xLabels: ['Q1', 'Q2', 'Q3', 'Q4'],
      areas: [
        { name: 'Revenue', data: [100, 150, 130, 200] },
        { name: 'Cost', data: [80, 90, 110, 120] },
      ],
    }]);
    assert.ok(canvas.height > 0);
  });

  it('scatter-chart', () => {
    const { canvas } = posterWith([{
      type: 'scatter-chart',
      title: 'Test Scatter',
      points: [
        { x: 1, y: 8 },
        { x: 3, y: 15, color: '#ef4444' },
        { x: 5, y: 22 },
        { x: 7, y: 18 },
      ],
    }]);
    assert.ok(canvas.height > 0);
  });

  it('all sections combined', () => {
    const { canvas } = posterWith([
      { type: 'kpi-cards', cards: [{ label: 'A', value: '1' }] },
      { type: 'bar-chart', bars: [{ name: 'X', value: 100 }] },
      { type: 'pie-chart', slices: [{ name: 'A', value: 50 }, { name: 'B', value: 50 }] },
      { type: 'line-chart', xLabels: ['A', 'B'], lines: [{ name: 'L', data: [10, 20] }] },
      { type: 'area-chart', xLabels: ['A', 'B'], areas: [{ name: 'A', data: [10, 20] }] },
      { type: 'scatter-chart', points: [{ x: 1, y: 2 }, { x: 3, y: 4 }] },
      { type: 'table', headers: ['H'], rows: [['R']] },
      { type: 'tips', items: ['T'] },
      { type: 'divider' },
    ]);
    assert.ok(canvas.height > 0);
  });
});

// ===== Height calculation consistency =====

describe('height calculation', () => {
  const sections = [
    { type: 'kpi-cards', cards: [{ label: 'A', value: '1' }, { label: 'B', value: '2' }, { label: 'C', value: '3' }] },
    { type: 'bar-chart', bars: [{ name: 'X', value: 100 }, { name: 'Y', value: 200 }] },
    { type: 'pie-chart', slices: [{ name: 'A', value: 30 }, { name: 'B', value: 70 }] },
    { type: 'line-chart', xLabels: ['A', 'B', 'C'], lines: [{ name: 'L1', data: [10, 20, 15] }] },
    { type: 'line-chart', xLabels: ['A', 'B'], lines: [{ name: 'L1', data: [10, 20] }, { name: 'L2', data: [5, 15] }] },
    { type: 'area-chart', xLabels: ['A', 'B', 'C'], areas: [{ name: 'A1', data: [10, 20, 15] }] },
    { type: 'area-chart', xLabels: ['A', 'B'], areas: [{ name: 'A1', data: [10, 20] }, { name: 'A2', data: [5, 15] }] },
    { type: 'scatter-chart', points: [{ x: 1, y: 2 }, { x: 3, y: 4 }] },
    { type: 'table', headers: ['H1', 'H2'], rows: [['a', 'b'], ['c', 'd']] },
    { type: 'tips', items: ['tip1', 'tip2'] },
    { type: 'divider' },
  ];

  for (const sec of sections) {
    it(`${sec.type} predicted height matches actual`, () => {
      const predicted = sectionHeight(sec);
      const canvas = createCanvas(800, 2000);
      const ctx = canvas.getContext('2d');
      const yStart = 100;
      const yEnd = drawSection(ctx, sec, yStart, 800);
      const actual = yEnd - yStart;
      assert.ok(
        Math.abs(predicted - actual) <= 2,
        `${sec.type}: predicted=${predicted}, actual=${actual}, diff=${Math.abs(predicted - actual)}`
      );
    });
  }
});

// ===== Empty data does not crash =====

describe('empty data', () => {
  it('empty cards', () => {
    assert.doesNotThrow(() => posterWith([{ type: 'kpi-cards', cards: [] }]));
  });
  it('empty bars', () => {
    assert.doesNotThrow(() => posterWith([{ type: 'bar-chart', bars: [] }]));
  });
  it('empty slices', () => {
    assert.doesNotThrow(() => posterWith([{ type: 'pie-chart', slices: [] }]));
  });
  it('empty table', () => {
    assert.doesNotThrow(() => posterWith([{ type: 'table', headers: [], rows: [] }]));
  });
  it('empty tips', () => {
    assert.doesNotThrow(() => posterWith([{ type: 'tips', items: [] }]));
  });
  it('empty lines', () => {
    assert.doesNotThrow(() => posterWith([{ type: 'line-chart', lines: [] }]));
  });
  it('empty areas', () => {
    assert.doesNotThrow(() => posterWith([{ type: 'area-chart', areas: [] }]));
  });
  it('empty points', () => {
    assert.doesNotThrow(() => posterWith([{ type: 'scatter-chart', points: [] }]));
  });
});

// ===== Auto file output =====

describe('auto file output', () => {
  it('writes PNG when output is set', () => {
    const out = tmpFile();
    try {
      const result = buildPoster({
        width: 400,
        sections: [{ type: 'kpi-cards', cards: [{ label: 'A', value: '1' }] }],
        output: out,
      });
      assert.ok(fs.existsSync(out), 'file should exist');
      const buf = fs.readFileSync(out);
      assert.ok(buf[0] === 0x89 && buf[1] === 0x50 && buf[2] === 0x4e && buf[3] === 0x47, 'should be valid PNG');
      assert.ok(result.buffer, 'result should include buffer');
      assert.equal(result.output, out);
    } finally {
      if (fs.existsSync(out)) fs.unlinkSync(out);
    }
  });

  it('does not include buffer when output is not set', () => {
    const result = buildPoster({
      width: 400,
      sections: [{ type: 'kpi-cards', cards: [{ label: 'A', value: '1' }] }],
    });
    assert.equal(result.buffer, undefined);
    assert.equal(result.output, undefined);
  });
});

// ===== Backward compatibility (data field) =====

describe('backward compatibility', () => {
  it('kpi-cards with data field', () => {
    assert.doesNotThrow(() => posterWith([{
      type: 'kpi-cards',
      data: [{ label: 'A', value: '1' }],
    }]));
  });

  it('bar-chart with data field', () => {
    assert.doesNotThrow(() => posterWith([{
      type: 'bar-chart',
      data: [{ name: 'X', value: 100 }],
    }]));
  });

  it('pie-chart with data field', () => {
    assert.doesNotThrow(() => posterWith([{
      type: 'pie-chart',
      data: [{ name: 'A', value: 50 }],
    }]));
  });

  it('table with data field (rows)', () => {
    assert.doesNotThrow(() => posterWith([{
      type: 'table',
      headers: ['H'],
      data: [['R']],
    }]));
  });

  it('tips with data field', () => {
    assert.doesNotThrow(() => posterWith([{
      type: 'tips',
      data: ['tip1'],
    }]));
  });

  it('line-chart with data field', () => {
    assert.doesNotThrow(() => posterWith([{
      type: 'line-chart',
      data: [{ name: 'L', data: [1, 2, 3] }],
    }]));
  });

  it('area-chart with data field', () => {
    assert.doesNotThrow(() => posterWith([{
      type: 'area-chart',
      data: [{ name: 'A', data: [1, 2, 3] }],
    }]));
  });

  it('scatter-chart with data field', () => {
    assert.doesNotThrow(() => posterWith([{
      type: 'scatter-chart',
      data: [{ x: 1, y: 2 }, { x: 3, y: 4 }],
    }]));
  });
});
