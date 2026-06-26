#!/usr/bin/env node
/**
 * OpenClaw Skill: arch-cad-generator
 * 中国规范 CAD 图纸生成器 - 核心绘制引擎
 *
 * 使用 makerjs（Photon 前身）进行程序化绘图，输出 SVG + PDF。
 * 严格遵循 GB/T 50104-2010《建筑制图标准》及 GB/T 50001-2017《房屋建筑制图统一标准》。
 */

const makerjs = require('makerjs');
const fs = require('fs');
const path = require('path');

// ============================================================
// 一、规范常量定义
// ============================================================

/** GB/T 50001-2017 图纸幅面 (mm) */
const PAPER_SIZES = {
  A0: [1189, 841],
  A1: [841, 594],
  A2: [594, 420],
  A3: [420, 297],
  A4: [297, 210],
};

/** GB/T 50104-2010 线宽组 (mm), 以 b=1.0 为基准 */
const LINE_WEIGHTS = {
  BOLD:      1.0,   // b — 粗实线：剖切到的墙体轮廓
  MEDIUM:    0.5,   // 0.5b — 中实线：可见轮廓
  THIN:      0.25,  // 0.25b — 细实线：尺寸线、轴线
};

/** GB 55038-2025 + GB 50096-2011 关键尺寸 (mm) */
const REGULATIONS = {
  MIN_STOREY_HEIGHT:       3000,   // 住宅层高 ≥ 3.0m (GB 55038-2025)
  MIN_BEDROOM_AREA_SQ:     9.0,    // 双人卧室 ≥ 9㎡ (GB 50096-2011)
  MIN_LIVING_AREA_SQ:      10.0,   // 起居室 ≥ 10㎡ (GB 50096-2011)
  MIN_KITCHEN_AREA_SQ:     4.0,    // 厨房 ≥ 4㎡ (GB 50096-2011)
  MIN_BATHROOM_AREA_SQ:    2.5,    // 卫生间 ≥ 2.5㎡ (GB 50096-2011)
  MAIN_DOOR_WIDTH:         900,    // 户门净宽 ≥ 0.90m (GB 55038-2025)
  BEDROOM_DOOR_WIDTH:      800,    // 卧室门 ≥ 0.80m
  BATH_DOOR_WIDTH:         700,    // 卫生间门 ≥ 0.70m
  CORRIDOR_WIDTH:          1200,   // 走廊净宽 ≥ 1.20m
  WALL_THICKNESS_OUTER:    240,    // 外墙厚度
  WALL_THICKNESS_INNER:    120,    // 内墙厚度
};

/** GB/T 50104-2010 图层名称 */
const LAYERS = {
  WALL:  'A-WALL',
  DOOR:  'A-DOOR',
  DIMS:  'A-DIMS',
  AXIS:  'A-AXIS',
  TEXT:  'A-TEXT',
  TTLB:  'A-TTLB',
  FURN:  'A-FURN',
};

// ============================================================
// 二、规范校验模块
// ============================================================

/**
 * 校验设计参数是否符合强制性规范
 * @param {Object} design - 用户设计参数
 * @returns {{ valid: boolean, violations: string[] }}
 */
function validateDesign(design) {
  const violations = [];
  const { rooms, storey_height } = design;

  if (storey_height && storey_height < REGULATIONS.MIN_STOREY_HEIGHT) {
    violations.push(
      `[GB 55038-2025] 层高 ${storey_height}mm < 最低要求 ${REGULATIONS.MIN_STOREY_HEIGHT}mm`
    );
  }

  for (const room of rooms || []) {
    const area = (room.width * room.height) / 1_000_000; // mm² → m²
    switch (room.type) {
      case 'bedroom':
        if (area < REGULATIONS.MIN_BEDROOM_AREA_SQ) {
          violations.push(
            `[GB 50096-2011] "${room.name}" 面积 ${area.toFixed(1)}㎡ < 最小 ${REGULATIONS.MIN_BEDROOM_AREA_SQ}㎡`
          );
        }
        break;
      case 'living':
        if (area < REGULATIONS.MIN_LIVING_AREA_SQ) {
          violations.push(
            `[GB 50096-2011] "${room.name}" 面积 ${area.toFixed(1)}㎡ < 最小 ${REGULATIONS.MIN_LIVING_AREA_SQ}㎡`
          );
        }
        break;
      case 'kitchen':
        if (area < REGULATIONS.MIN_KITCHEN_AREA_SQ) {
          violations.push(
            `[GB 50096-2011] "${room.name}" 面积 ${area.toFixed(1)}㎡ < 最小 ${REGULATIONS.MIN_KITCHEN_AREA_SQ}㎡`
          );
        }
        break;
      case 'bathroom':
        if (area < REGULATIONS.MIN_BATHROOM_AREA_SQ) {
          violations.push(
            `[GB 50096-2011] "${room.name}" 面积 ${area.toFixed(1)}㎡ < 最小 ${REGULATIONS.MIN_BATHROOM_AREA_SQ}㎡`
          );
        }
        break;
    }
  }

  return { valid: violations.length === 0, violations };
}

// ============================================================
// 三、图纸绘制模块
// ============================================================

/**
 * 创建定位轴线（细点划线, GB/T 50104-2010）
 * @param {number} x - 轴线位置 X
 * @param {number} y - 轴线位置 Y
 * @param {number} length - 轴线长度
 * @param {'h'|'v'} direction - 水平/垂直
 * @returns {makerjs.paths.Line}
 */
function createAxis(x, y, length, direction) {
  const isHorizontal = direction === 'h';
  const path = new makerjs.paths.Line(
    [x, y],
    [isHorizontal ? x + length : x, isHorizontal ? y : y + length]
  );
  path.layer = LAYERS.AXIS;
  return path;
}

/**
 * 创建墙体（粗实线, GB/T 50104-2010）
 * @returns {makerjs.models.ConnectTheDots}
 */
function createWall(points, thickness) {
  // 外墙为矩形，用粗实线绘制
  const wallModel = new makerjs.models.ConnectTheDots(true, points);
  wallModel.layer = LAYERS.WALL;
  wallModel.paths.forEach(p => {
    p.layer = LAYERS.WALL;
  });
  return wallModel;
}

/**
 * 创建墙体矩形（简化版：给定对角两点）
 */
function createWallRect(x1, y1, x2, y2) {
  const model = new makerjs.models.ConnectTheDots(true, [
    [x1, y1], [x2, y1], [x2, y2], [x1, y2]
  ]);
  model.layer = LAYERS.WALL;
  return model;
}

/**
 * 创建门（中实线 + 开启弧线, GB/T 50104-2010）
 * @param {number} x, y - 门铰链位置
 * @param {number} width - 门宽
 * @param {'l'|'r'|'u'|'d'} swing - 开启方向
 */
function createDoor(x, y, width, swing) {
  const doorModel = new makerjs.models.ConnectTheDots(true, [
    [x, y], [x, y + width]
  ]);
  doorModel.layer = LAYERS.DOOR;
  return doorModel;
}

/**
 * 创建窗户（四条细线表示窗, GB/T 50104-2010）
 */
function createWindow(x1, y1, x2, y2) {
  const model = {
    paths: {
      outer1: new makerjs.paths.Line([x1, y1], [x2, y1]),
      outer2: new makerjs.paths.Line([x1, y2], [x2, y2]),
      inner1: new makerjs.paths.Line([x1, (y1 + y2) / 2 - 25], [x2, (y1 + y2) / 2 - 25]),
      inner2: new makerjs.paths.Line([x1, (y1 + y2) / 2 + 25], [x2, (y1 + y2) / 2 + 25]),
    },
  };
  Object.values(model.paths).forEach(p => { p.layer = LAYERS.DOOR; });
  return model;
}

/**
 * 创建图框和标题栏（GB/T 50001-2017）
 * @param {[number,number]} paperSize - [宽, 高] mm
 */
function createTitleBlock(paperSize) {
  const [pw, ph] = paperSize;
  const model = {
    paths: {},
  };

  // 外框（细实线）
  model.paths.outerFrame = new makerjs.paths.Line([0, 0], [pw, 0]);
  model.paths.outerFrame.layer = LAYERS.TTLB;
  // ...（实际项目中应绘制完整的标题栏，此处示意）

  return model;
}

// ============================================================
// 四、尺寸标注模块（GB/T 50104-2010）
// ============================================================

/**
 * 创建尺寸标注线（细实线 + 起止符号）
 * @param {number} x1, y1 - 标注起点
 * @param {number} x2, y2 - 标注终点
 * @param {string} text - 标注文字
 * @param {number} offset - 与标注对象的间距
 */
function createDimension(x1, y1, x2, y2, text, offset) {
  const dimModel = {
    paths: {
      dimLine: new makerjs.paths.Line([x1, y1 - offset], [x2, y2 - offset]),
      tick1:    new makerjs.paths.Line([x1, y1 - offset - 50], [x1, y1 - offset + 50]),
      tick2:    new makerjs.paths.Line([x2, y2 - offset - 50], [x2, y2 - offset + 50]),
    },
  };
  Object.values(dimModel.paths).forEach(p => { p.layer = LAYERS.DIMS; });
  return dimModel;
}

// ============================================================
// 五、完整平面图生成
// ============================================================

/**
 * 生成住宅平面图
 * @param {Object} design - { rooms, width, height, scale, paperSize }
 * @returns {makerjs.Drawing}
 */
function generateFloorPlan(design) {
  const drawing = new makerjs.Drawing();

  // --- 1. 定位轴线 ---
  const axisSpacing = 3000; // 轴线间距 3m（与层高一致）
  const numAxisH = Math.ceil(design.height / axisSpacing) + 1;
  const numAxisV = Math.ceil(design.width / axisSpacing) + 1;

  for (let i = 0; i < numAxisH; i++) {
    const y = i * axisSpacing;
    const axis = createAxis(-500, y, design.width + 1000, 'h');
    drawing.addPath(axis);
  }
  for (let i = 0; i < numAxisV; i++) {
    const x = i * axisSpacing;
    const axis = createAxis(x, -500, design.height + 1000, 'v');
    drawing.addPath(axis);
  }

  // --- 2. 墙体 ---
  // 外墙
  drawing.addModel(createWallRect(
    0, 0,
    design.width, design.height
  ));

  // --- 3. 房间分隔墙 ---
  let xCursor = 0;
  for (const room of design.rooms || []) {
    const rx = xCursor;
    const ry = 0;
    const rw = room.width;
    const rh = room.height;

    // 内墙
    if (xCursor > 0) {
      drawing.addModel(createWallRect(
        xCursor - REGULATIONS.WALL_THICKNESS_INNER / 2, ry,
        xCursor + REGULATIONS.WALL_THICKNESS_INNER / 2, rh
      ));
    }

    // 门（根据房间类型设置门宽）
    let doorWidth = REGULATIONS.BEDROOM_DOOR_WIDTH;
    if (room.type === 'bathroom') doorWidth = REGULATIONS.BATH_DOOR_WIDTH;

    const door = createDoor(rx + 200, ry + rh / 2 - doorWidth / 2, doorWidth, 'r');
    drawing.addModel(door);

    xCursor += room.width;
  }

  // --- 4. 尺寸标注 ---
  drawing.addModel(createDimension(0, 0, design.width, 0,
    `${(design.width / 1000).toFixed(2)}m`, 800));
  drawing.addModel(createDimension(0, 0, 0, design.height,
    `${(design.height / 1000).toFixed(2)}m`, 800));

  // --- 5. 图框 ---
  drawing.addModel(createTitleBlock(design.paperSize));

  return drawing;
}

// ============================================================
// 六、输出模块
// ============================================================

/**
 * 导出图纸到文件
 * @param {makerjs.Drawing} drawing
 * @param {Object} options - { format, outputDir, filename }
 */
function exportDrawing(drawing, options) {
  const { format, outputDir, filename } = options;
  const outDir = outputDir || './output';

  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  if (format === 'svg' || format === 'both') {
    const svg = makerjs.exporter.toSVG(drawing, {
      useSvgPathOnly: false,
      strokeWidth: 0.25,
    });
    fs.writeFileSync(path.join(outDir, `${filename}.svg`), svg);
    console.log(`✅ SVG 已输出: ${outDir}/${filename}.svg`);
  }

  if (format === 'pdf' || format === 'both') {
    const pdf = makerjs.exporter.toPDF(drawing, {
      pageSize: drawing.paperSize || [420, 297],
    });
    fs.writeFileSync(path.join(outDir, `${filename}.pdf`), pdf);
    console.log(`✅ PDF 已输出: ${outDir}/${filename}.pdf`);
  }
}

// ============================================================
// 七、主入口
// ============================================================

async function main() {
  // 从命令行参数或环境变量读取设计参数
  const args = process.argv.slice(2);

  // 默认：90㎡ 两室一厅
  const design = {
    storey_height: 3000,
    width:  9000,  // 9m 面宽
    height: 10000, // 10m 进深
    scale:  100,   // 1:100
    paperSize: PAPER_SIZES.A3,
    rooms: [
      { name: '客厅', type: 'living',   width: 4500, height: 5000 },
      { name: '主卧', type: 'bedroom',  width: 3500, height: 4500 },
      { name: '次卧', type: 'bedroom',  width: 3000, height: 3500 },
      { name: '厨房', type: 'kitchen',  width: 2000, height: 3000 },
      { name: '卫生间', type: 'bathroom', width: 2000, height: 2500 },
    ],
  };

  // --- 规范校验 ---
  const { valid, violations } = validateDesign(design);
  if (!valid) {
    console.warn('⚠️  设计存在以下规范违规：');
    violations.forEach(v => console.warn(`   - ${v}`));
    console.warn('将继续生成图纸，但请在设计说明中注明偏差。\n');
  } else {
    console.log('✅ 设计通过强制性规范校验。\n');
  }

  // --- 生成图纸 ---
  console.log('🔧 正在生成图纸...');
  const drawing = generateFloorPlan(design);

  // --- 输出 ---
  exportDrawing(drawing, {
    format: 'both',
    outputDir: './output',
    filename: `floor-plan-${Date.now()}`,
  });

  console.log('🎉 图纸生成完成！');
  return { success: true, violations };
}

// 执行
main().catch(err => {
  console.error('❌ 图纸生成失败:', err.message);
  process.exit(1);
});