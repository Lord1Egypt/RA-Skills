/**
 * 风水堪舆 Skill - 核心算法
 * 作者：天工长老
 * 版本：v1.1
 * 创建：2026 年 3 月 29 日
 * 更新：2026 年 3 月 30 日 - 添加玄空飞星基础、二十四山详解
 */

// 命卦计算
function calcMingGua(year, gender) {
  const yearLast2 = year % 100;
  let remainder;
  
  if (gender === 'male') {
    remainder = (100 - yearLast2) % 9;
  } else {
    remainder = (yearLast2 - 4) % 9;
  }
  
  if (remainder <= 0) remainder += 9;
  
  const guaMap = {
    1: '坎', 2: '坤', 3: '震', 4: '巽',
    5: gender === 'male' ? '坤' : '艮',
    6: '乾', 7: '兑', 8: '艮', 9: '离'
  };
  
  return guaMap[remainder];
}

// 东四命/西四命判断
function getMingType(mingGua) {
  const dongSi = ['坎', '离', '震', '巽'];
  const xiSi = ['乾', '坤', '艮', '兑'];
  
  if (dongSi.includes(mingGua)) return '东四命';
  if (xiSi.includes(mingGua)) return '西四命';
  return '未知';
}

// 宅型判断（根据坐向）
function getZhaiType(direction) {
  const directionMap = {
    '北': '坎宅', '南': '离宅', '东': '震宅', '西': '兑宅',
    '东北': '艮宅', '西北': '乾宅', '东南': '巽宅', '西南': '坤宅'
  };
  return directionMap[direction] || '未知';
}

// 游年九星排布（简化版）
function getJiuXing(mingGua) {
  const jiuXingMap = {
    '坎': {
      生气：'东南', 天医：'东', 延年：'南', 伏位：'北',
      祸害：'西', 六煞：'西北', 五鬼：'东北', 绝命：'西南'
    },
    '离': {
      生气：'东', 天医：'东南', 延年：'北', 伏位：'南',
      祸害：'西南', 六煞：'东', 五鬼：'西', 绝命：'西北'
    },
    '震': {
      生气：'南', 天医：'北', 延年：'东南', 伏位：'东',
      祸害：'西南', 六煞：'东北', 五鬼：'西北', 绝命：'西'
    },
    '巽': {
      生气：'北', 天医：'南', 延年：'东', 伏位：'东南',
      祸害：'东', 六煞：'西', 五鬼：'西南', 绝命：'东北'
    },
    '乾': {
      生气：'西', 天医：'东北', 延年：'西南', 伏位：'西北',
      祸害：'东南', 六煞：'北', 五鬼：'东', 绝命：'南'
    },
    '坤': {
      生气：'东北', 天医：'西', 延年：'西北', 伏位：'西南',
      祸害：'北', 六煞：'南', 五鬼：'东南', 绝命：'北'
    },
    '艮': {
      生气：'西南', 天医：'西北', 延年：'西', 伏位：'东北',
      祸害：'南', 六煞：'东', 五鬼：'北', 绝命：'东南'
    },
    '兑': {
      生气：'西北', 天医：'西南', 延年：'东北', 伏位：'西',
      祸害：'北', 六煞：'东南', 五鬼：'南', 绝命：'东'
    }
  };
  
  return jiuXingMap[mingGua] || {};
}

// 九星吉凶判断
function getJiuXingJiXiong(star) {
  const jiXiong = {
    '生气': '大吉', '天医': '吉', '延年': '吉', '伏位': '小吉',
    '祸害': '凶', '六煞': '凶', '五鬼': '大凶', '绝命': '大凶'
  };
  return jiXiong[star] || '平';
}

// 宅命匹配判断
function matchZhaiMing(mingGua, zhaiType) {
  const dongSiZhai = ['坎宅', '离宅', '震宅', '巽宅'];
  const xiSiZhai = ['乾宅', '坤宅', '艮宅', '兑宅'];
  const dongSiMing = ['坎', '离', '震', '巽'];
  const xiSiMing = ['乾', '坤', '艮', '兑'];
  
  const isDongSiMing = dongSiMing.includes(mingGua);
  const isDongSiZhai = dongSiZhai.includes(zhaiType);
  
  if (isDongSiMing && isDongSiZhai) return { match: true, msg: '吉（东四命住东四宅）' };
  if (!isDongSiMing && !isDongSiZhai) return { match: true, msg: '吉（西四命住西四宅）' };
  return { match: false, msg: '凶（宅命不配）' };
}

// 布局建议
function getBuJuJianYi(jiuXing) {
  const jiFang = [];
  const xiongFang = [];
  
  for (const [star, fangwei] of Object.entries(jiuXing)) {
    const jiXiong = getJiuXingJiXiong(star);
    if (jiXiong.includes('吉')) {
      jiFang.push({ 方位：fangwei, 星：star, 吉凶：jiXiong });
    } else {
      xiongFang.push({ 方位：fangwei, 星：star, 吉凶：jiXiong });
    }
  }
  
  return {
    吉方：jiFang,
    凶方：xiongFang,
    建议：{
      卧室：'宜在生气、天医、延年方',
      大门：'宜开在生气、延年方',
      厨房：'宜压在凶方，灶口向吉方',
      卫生间：'不宜在吉方',
      客厅：'宜在生气、伏位方'
    }
  };
}

// 综合风水分析
function fengShui(year, gender, direction) {
  const mingGua = calcMingGua(year, gender);
  const mingType = getMingType(mingGua);
  const zhaiType = getZhaiType(direction);
  const match = matchZhaiMing(mingGua, zhaiType);
  const jiuXing = getJiuXing(mingGua);
  const buJu = getBuJuJianYi(jiuXing);
  
  // 综合评分
  let score = 60;
  if (match.match) score += 25;
  else score -= 20;
  
  let conclusion = '中';
  if (score >= 80) conclusion = '吉';
  else if (score >= 65) conclusion = '中吉';
  else if (score >= 50) conclusion = '中';
  else conclusion = '凶';
  
  return {
    命主信息：{
      出生年份：year,
      性别：gender === 'male' ? '男' : '女',
      命卦：mingGua,
      命型：mingType
    },
    宅型信息：{
      坐向：direction,
      宅型：zhaiType
    },
    宅命匹配：match,
    游年九星：jiuXing,
    布局建议：buJu,
    综合评分：score,
    综合判断：conclusion
  };
}

// 导出
module.exports = {
  fengShui,
  calcMingGua,
  getMingType,
  getZhaiType,
  getJiuXing,
  matchZhaiMing,
  getBuJuJianYi,
  // v1.1 新增
  getErShiSiShan,
  getXuanKongFeiXing
};

// ========== v1.1 新增：二十四山详解 ==========

// 二十四山
const ER_SHI_SI_SHAN = {
  北：['壬', '子', '癸'],
  东北：['丑', '艮', '寅'],
  东：['甲', '卯', '乙'],
  东南：['辰', '巽', '巳'],
  南：['丙', '午', '丁'],
  西南：['未', '坤', '申'],
  西：['庚', '酉', '辛'],
  西北：['戌', '乾', '亥']
};

// 获取二十四山详情
function getErShiSiShan(fangWei) {
  if (ER_SHI_SI_SHAN[fangWei]) {
    return {
      方位：fangWei,
      三山：ER_SHI_SI_SHAN[fangWei],
      五行：getShanWuXing(fangWei)
    };
  }
  return null;
}

// 山的五行
function getShanWuXing(fangWei) {
  const wuXingMap = {
    北：'水', 东北：'土', 东：'木', 东南：'木',
    南：'火', 西南：'土', 西：'金', 西北：'金'
  };
  return wuXingMap[fangWei] || '未知';
}

// 玄空飞星基础（简化版）
function getXuanKongFeiXing(year, fangWei) {
  // 九宫飞星顺序
  const feiXing = [
    '一白贪狼', '二黑巨门', '三碧禄存', '四绿文曲',
    '五黄廉贞', '六白武曲', '七赤破军', '八白左辅', '九紫右弼'
  ];
  
  // 年飞星（简化计算）
  const yearStarIndex = (year - 1900) % 9;
  const yearStar = feiXing[yearStarIndex];
  
  // 方位飞星
  const fangWeiIndex = Object.keys(ER_SHI_SI_SHAN).indexOf(fangWei);
  const fangWeiStar = feiXing[(yearStarIndex + fangWeiIndex) % 9];
  
  return {
    年份：year,
    年飞星：yearStar,
    方位：fangWei,
    方位飞星：fangWeiStar,
    吉凶：getFeiXingJiXiong(fangWeiStar)
  };
}

// 飞星吉凶
function getFeiXingJiXiong(feiXing) {
  const jiXing = ['一白贪狼', '四绿文曲', '六白武曲', '八白左辅', '九紫右弼'];
  const xiongXing = ['二黑巨门', '三碧禄存', '五黄廉贞', '七赤破军'];
  
  if (jiXing.includes(feiXing)) return '吉';
  if (xiongXing.includes(feiXing)) return '凶';
  return '平';
}
