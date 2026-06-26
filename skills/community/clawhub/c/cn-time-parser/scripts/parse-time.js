#!/usr/bin/env node

import dayjs from 'dayjs';
import lunisolar from 'lunisolar';
import { ArgumentParser } from 'argparse';
import * as chineseWorkday from 'chinese-workday';

const { isWorkday, isHoliday, getFestival } = chineseWorkday;

const parser = new ArgumentParser({
  description: '时间解析器 - 识别中文时间关键词并转换为具体日期'
});

parser.add_argument('--query', { help: '包含时间关键词的用户提问', required: true });

const args = parser.parse_args();

// 中文数字映射
const chineseNumbers = {
  '零': 0, '〇': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, 
  '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10, 
  '廿': 20, '卅': 30
};

// 解析中文数字
function parseChineseNumber(text) {
  if (!text) return null;
  
  // 特殊处理"正月"
  if (text === '正') return 1;
  
  // 直接是阿拉伯数字
  if (/^\d+$/.test(text)) {
    return parseInt(text);
  }
  
  // 中文数字解析
  let result = 0;
  let temp = 0;
  
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    if (char === '十') {
      if (temp === 0) temp = 1;
      result += temp * 10;
      temp = 0;
    } else if (char === '廿') {
      result += 20;
    } else if (char === '卅') {
      result += 30;
    } else if (chineseNumbers[char] !== undefined) {
      temp = chineseNumbers[char];
    }
  }
  result += temp;
  
  return result > 0 ? result : null;
}

// 解析农历日期
function parseLunarDate(query, baseYear) {
  // 预处理：将"正月"替换为"一月"便于匹配
  let processedQuery = query.replace(/正月/g, '一月');
  
  // 匹配模式：农历[年份]?[闰]?[月份][初/一/二/...][日]
  const lunarPatterns = [
    // 带年份的模式：农历2024年二月二十五（优先级最高）
    {
      regex: /农历(\d{4})年?(?:闰)?(\S+?)月(\S+?)(?=$|[，。！？、；：""''（）【】\s]|日|号)/,
      handler: (match) => {
        const year = parseInt(match[1]);
        // 处理"正月"
        const monthStr = match[2] === '正' ? '一' : match[2];
        const month = parseChineseNumber(monthStr);
        const day = parseChineseNumber(match[3]);
        const isLeap = match[0].includes('闰');
        return { year, month, day, isLeap, fullMatch: match[0] };
      }
    },
    // 完整模式：明年农历二月二十五（两种变体）
    {
      regex: /(今年|去年|明年|后年|前年).*?农历(?:闰)?(\S+?)月(\S+?)(?=$|[，。！？、；：""''（）【】\s]|日|号)/,
      handler: (match) => {
        const yearModifier = match[1];
        let year = baseYear;
        if (yearModifier === '去年') year -= 1;
        if (yearModifier === '明年') year += 1;
        if (yearModifier === '后年') year += 2;
        if (yearModifier === '前年') year -= 2;
        
        // 处理"正月"
        const monthStr = match[2] === '正' ? '一' : match[2];
        const month = parseChineseNumber(monthStr);
        const day = parseChineseNumber(match[3]);
        const isLeap = match[0].includes('闰');
        return { year, month, day, isLeap, fullMatch: match[0] };
      }
    },
    // 变体：农历明年二月二十五
    {
      regex: /农历(今年|去年|明年|后年|前年)(?:闰)?(\S+?)月(\S+?)(?=$|[，。！？、；：""''（）【】\s]|日|号)/,
      handler: (match) => {
        const yearModifier = match[1];
        let year = baseYear;
        if (yearModifier === '去年') year -= 1;
        if (yearModifier === '明年') year += 1;
        if (yearModifier === '后年') year += 2;
        if (yearModifier === '前年') year -= 2;
        
        // 处理"正月"
        const monthStr = match[2] === '正' ? '一' : match[2];
        const month = parseChineseNumber(monthStr);
        const day = parseChineseNumber(match[3]);
        const isLeap = match[0].includes('闰');
        return { year, month, day, isLeap, fullMatch: match[0] };
      }
    },
    // 简单模式：农历二月二十五（优先级最低）
    {
      regex: /农历(?:闰)?(\S+?)月(\S+?)(?=$|[，。！？、；：""''（）【】\s]|日|号)/,
      handler: (match) => {
        const month = parseChineseNumber(match[1]);
        const day = parseChineseNumber(match[2]);
        const isLeap = match[0].includes('闰');
        return { year: baseYear, month, day, isLeap, fullMatch: match[0] };
      }
    }
  ];

  for (const pattern of lunarPatterns) {
    const match = processedQuery.match(pattern.regex);
    if (match) {
      try {
        const lunarData = pattern.handler(match);
        if (lunarData && lunarData.month && lunarData.day) {
          const lunarDate = lunisolar.fromLunar({
            year: lunarData.year,
            month: lunarData.month,
            day: lunarData.day,
            isLeapMonth: lunarData.isLeap
          });
          // 从原始query中提取匹配的关键词，保持"正月"的原貌
          let matchedKeyword = lunarData.fullMatch || match[0];
          if (query.includes('正月') && matchedKeyword.includes('一月')) {
            matchedKeyword = matchedKeyword.replace('一月', '正月');
          }
          
          return {
            date: dayjs(lunarDate.toDate()),
            matchedKeyword: matchedKeyword,
            lunarData: lunarData
          };
        }
      } catch (error) {
        console.error('解析农历日期时出错:', error);
      }
    }
  }
  
  return null;
}

// 节日名称映射
const festivalNameMap = {
  '元旦': '元旦',
  '春节': '春节',
  '过年': '春节',
  '五一': '劳动节',
  '劳动节': '劳动节',
  '国庆': '国庆节',
  '十一': '国庆节'
};

// 已知节日的固定日期映射（作为备用）
const fixedFestivalDates = {
  '元旦': (year) => dayjs(`${year}-01-01`),
  '劳动节': (year) => dayjs(`${year}-05-01`),
  '国庆节': (year) => dayjs(`${year}-10-01`),
  '春节': (year) => getSpringFestival(year)
};

// 获取节日日期
function getFestivalDate(year, festivalName) {
  // 标准化节日名称
  const normalizedName = festivalNameMap[festivalName] || festivalName;
  
  // 对于有固定日期的节日，直接返回
  if (fixedFestivalDates[normalizedName]) {
    return fixedFestivalDates[normalizedName](year);
  }
  
  // 备用方法
  return getSpringFestival(year);
}

function parseTimeQuery(query) {
  const now = dayjs();
  let result = {
    success: false,
    originalQuery: query,
    parsedDate: null,
    timestamp: null,
    lunarInfo: null,
    festivalInfo: null,
    isWorkday: null,
    isHoliday: null,
    matchedKeyword: null
  };

  // 首先尝试解析农历日期（优先级最高）
  const lunarResult = parseLunarDate(query, now.year());
  if (lunarResult) {
    const date = lunarResult.date;
    result.success = true;
    result.parsedDate = date.format('YYYY-MM-DD');
    result.timestamp = date.valueOf();
    result.matchedKeyword = lunarResult.matchedKeyword;
    
    // 获取农历信息
    try {
      const lunar = lunisolar(date.toDate());
      result.lunarInfo = {
        year: lunar.lunarYear,
        month: lunar.lunarMonth,
        day: lunar.lunarDay,
        isLeapMonth: lunar.isLeapMonth,
        zodiac: lunar.yearZodiac ? lunar.yearZodiac.name : null,
        term: lunar.solarTerm ? lunar.solarTerm.name : null
      };
    } catch (e) {
      console.error('获取农历信息时出错:', e);
    }
    
    // 获取节日和工作日信息
    try {
      result.festivalInfo = getFestival(date.toDate());
      result.isWorkday = isWorkday(date.toDate());
      result.isHoliday = isHoliday(date.toDate());
    } catch (e) {
      console.error('获取节日信息时出错:', e);
    }
    
    return result;
  }

  // 基础时间关键词
  const keywords = [
    { regex: /今天/, handler: () => now },
    { regex: /昨天/, handler: () => now.subtract(1, 'day') },
    { regex: /明天/, handler: () => now.add(1, 'day') },
    { regex: /前天/, handler: () => now.subtract(2, 'day') },
    { regex: /后天/, handler: () => now.add(2, 'day') },
    { regex: /大前天/, handler: () => now.subtract(3, 'day') },
    { regex: /大后天/, handler: () => now.add(3, 'day') },
    { regex: /今年/, handler: () => now.startOf('year') },
    { regex: /去年/, handler: () => now.subtract(1, 'year').startOf('year') },
    { regex: /明年/, handler: () => now.add(1, 'year').startOf('year') }
  ];

  // 节日关键词
  const festivalKeywords = [
    { regex: /今年春节|今年过年/, handler: () => getFestivalDate(now.year(), '春节') },
    { regex: /去年春节|去年过年/, handler: () => getFestivalDate(now.year() - 1, '春节') },
    { regex: /明年春节|明年过年/, handler: () => getFestivalDate(now.year() + 1, '春节') },
    { regex: /今年五一/, handler: () => getFestivalDate(now.year(), '五一') },
    { regex: /去年五一/, handler: () => getFestivalDate(now.year() - 1, '五一') },
    { regex: /明年五一/, handler: () => getFestivalDate(now.year() + 1, '五一') },
    { regex: /今年十一|今年国庆/, handler: () => getFestivalDate(now.year(), '国庆') },
    { regex: /去年十一|去年国庆/, handler: () => getFestivalDate(now.year() - 1, '国庆') },
    { regex: /明年十一|明年国庆/, handler: () => getFestivalDate(now.year() + 1, '国庆') },
    { regex: /今年元旦/, handler: () => getFestivalDate(now.year(), '元旦') },
    { regex: /去年元旦/, handler: () => getFestivalDate(now.year() - 1, '元旦') },
    { regex: /明年元旦/, handler: () => getFestivalDate(now.year() + 1, '元旦') }
  ];

  // 合并所有关键词，节日关键词在前（更长的关键词优先匹配）
  const allKeywords = [...festivalKeywords, ...keywords];

  // 匹配关键词
  for (const keyword of allKeywords) {
    if (keyword.regex.test(query)) {
      try {
        const date = keyword.handler();
        result.success = true;
        result.parsedDate = date.format('YYYY-MM-DD');
        result.timestamp = date.valueOf();
        result.matchedKeyword = query.match(keyword.regex)[0];
        
        // 尝试获取农历信息
        try {
          const lunar = lunisolar(date.toDate());
          result.lunarInfo = {
            year: lunar.lunarYear,
            month: lunar.lunarMonth,
            day: lunar.lunarDay,
            isLeapMonth: lunar.isLeapMonth,
            zodiac: lunar.yearZodiac ? lunar.yearZodiac.name : null,
            term: lunar.solarTerm ? lunar.solarTerm.name : null
          };
        } catch (e) {
          console.error('获取农历信息时出错:', e);
        }
        
        // 获取节日和工作日信息
        try {
          result.festivalInfo = getFestival(date.toDate());
          result.isWorkday = isWorkday(date.toDate());
          result.isHoliday = isHoliday(date.toDate());
        } catch (e) {
          console.error('获取节日信息时出错:', e);
        }
        
        break;
      } catch (error) {
        console.error('处理时间关键词时出错:', error);
      }
    }
  }

  return result;
}

// 获取春节日期（农历正月初一）- 备用方法
function getSpringFestival(year) {
  try {
    // 农历正月初一 - 使用正确的lunisolar API
    const lunarNewYear = lunisolar.fromLunar({
      year: year,
      month: 1,
      day: 1,
      isLeapMonth: false
    });
    return dayjs(lunarNewYear.toDate());
  } catch (error) {
    console.error('获取春节日期时出错:', error);
    // 如果获取失败，返回一个近似值（通常春节在1月或2月）
    return dayjs(`${year}-02-01`);
  }
}

// 主函数
function main() {
  try {
    const result = parseTimeQuery(args.query);
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('解析时间时出错:', error);
    console.log(JSON.stringify({
      success: false,
      error: error.message,
      originalQuery: args.query
    }, null, 2));
  }
}

main();
