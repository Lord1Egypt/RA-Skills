/**
 * benchmark-recall.ts — 无向量召回基准测试
 * 用法: npx tsx cc-soul/benchmark-recall.ts
 */

import { createRequire } from 'module'
import { fileURLToPath } from 'url'
import type { Memory } from './types.ts'

const require = createRequire(import.meta.url)
;(globalThis as any).require = require
process.env.CC_SOUL_BENCHMARK = "1"  // activation-field.ts 内部 12 处 require 需要

// Lazy-load modules to avoid side effects
const { activationRecall } = require('./activation-field.ts')
const { expandQuery, learnAssociation } = require('./aam.ts')

// ═══════════════════════════════════════════════════════════════
// TEST DATA: 200 memories (index 0-199)
// ═══════════════════════════════════════════════════════════════

const TEST_MEMORIES: Memory[] = [
  // ── 0-19: Original batch ──
  { content: '我在字节跳动做后端开发，主要写 Go 语言', scope: 'fact', ts: Date.now() - 86400000 * 30, confidence: 0.9, recallCount: 5, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '我女朋友叫小雨，我们在一起三年了', scope: 'fact', ts: Date.now() - 86400000 * 60, confidence: 0.95, recallCount: 8, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '最近血压有点高，医生让我少吃盐', scope: 'fact', ts: Date.now() - 86400000 * 10, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '我养了一只橘猫叫橘子，特别能吃', scope: 'fact', ts: Date.now() - 86400000 * 90, confidence: 0.9, recallCount: 6, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '我大学在武汉读的计算机专业', scope: 'fact', ts: Date.now() - 86400000 * 120, confidence: 0.9, recallCount: 4, lastAccessed: Date.now() - 86400000 * 15 },
  { content: '去年十一去了成都旅游，吃了很多火锅', scope: 'episode', ts: Date.now() - 86400000 * 180, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 86400000 * 30 },
  { content: '我每天早上跑步 5 公里，坚持了三个月', scope: 'fact', ts: Date.now() - 86400000 * 45, confidence: 0.85, recallCount: 4, lastAccessed: Date.now() - 86400000 * 7 },
  { content: '最近在学 Rust，感觉所有权系统很难理解', scope: 'fact', ts: Date.now() - 86400000 * 5, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '我妈做的红烧肉特别好吃，每次回家都要吃', scope: 'fact', ts: Date.now() - 86400000 * 200, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - 86400000 * 20 },
  { content: '上周面试了阿里巴巴，二面被刷了', scope: 'episode', ts: Date.now() - 86400000 * 7, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '我有轻度失眠，一般凌晨一点才能睡着', scope: 'fact', ts: Date.now() - 86400000 * 20, confidence: 0.8, recallCount: 3, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '正在还房贷，每个月还 8000', scope: 'fact', ts: Date.now() - 86400000 * 60, confidence: 0.9, recallCount: 2, lastAccessed: Date.now() - 86400000 * 10 },
  { content: '小雨怀孕了，预产期是明年三月', scope: 'fact', ts: Date.now() - 86400000 * 3, confidence: 0.95, recallCount: 5, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '我喜欢看科幻电影，最喜欢星际穿越', scope: 'preference', ts: Date.now() - 86400000 * 150, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 30 },
  { content: '周末经常和朋友打篮球，在公司附近的球场', scope: 'fact', ts: Date.now() - 86400000 * 25, confidence: 0.8, recallCount: 3, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '我对花粉过敏，春天出门要戴口罩', scope: 'fact', ts: Date.now() - 86400000 * 300, confidence: 0.9, recallCount: 4, lastAccessed: Date.now() - 86400000 * 60 },
  { content: '最近在考虑买特斯拉 Model 3', scope: 'fact', ts: Date.now() - 86400000 * 2, confidence: 0.75, recallCount: 1, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '我老家在湖南长沙，特别能吃辣', scope: 'fact', ts: Date.now() - 86400000 * 365, confidence: 0.95, recallCount: 5, lastAccessed: Date.now() - 86400000 * 40 },
  { content: '下个月要参加朋友的婚礼，需要准备份子钱', scope: 'episode', ts: Date.now() - 86400000 * 1, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() },
  { content: '最近经常加班到十一点，感觉很累', scope: 'episode', ts: Date.now() - 86400000 * 3, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 86400000 * 1 },

  // ── 20-39: Second batch ──
  { content: '我每天早上 7 点起床跑步', scope: 'fact', ts: Date.now() - 86400000 * 15, confidence: 0.9, recallCount: 5, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '我对花粉过敏，春天不能出门', scope: 'fact', ts: Date.now() - 86400000 * 180, confidence: 0.9, recallCount: 4, lastAccessed: Date.now() - 86400000 * 30 },
  { content: '我的车是特斯拉 Model 3', scope: 'fact', ts: Date.now() - 86400000 * 50, confidence: 0.92, recallCount: 3, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '上个月工资涨了 2000', scope: 'fact', ts: Date.now() - 86400000 * 35, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 10 },
  { content: '我女儿在学钢琴，每周三上课', scope: 'fact', ts: Date.now() - 86400000 * 60, confidence: 0.9, recallCount: 4, lastAccessed: Date.now() - 86400000 * 7 },
  { content: '我戒烟第 47 天了', scope: 'fact', ts: Date.now() - 86400000 * 8, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '我最怕蛇', scope: 'fact', ts: Date.now() - 86400000 * 120, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - 86400000 * 20 },
  { content: '下个月要去日本旅游', scope: 'episode', ts: Date.now() - 86400000 * 5, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '我大学室友叫张磊，现在在腾讯', scope: 'fact', ts: Date.now() - 86400000 * 150, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 86400000 * 25 },
  { content: '我血型是 O 型', scope: 'fact', ts: Date.now() - 86400000 * 200, confidence: 0.95, recallCount: 1, lastAccessed: Date.now() - 86400000 * 60 },
  { content: '周末一般陪孩子去公园', scope: 'fact', ts: Date.now() - 86400000 * 40, confidence: 0.85, recallCount: 4, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '我在考虑换工作，目标是阿里', scope: 'fact', ts: Date.now() - 86400000 * 3, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '我炒股亏了 3 万', scope: 'fact', ts: Date.now() - 86400000 * 25, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 86400000 * 8 },
  { content: '我正在学日语，N3 水平', scope: 'fact', ts: Date.now() - 86400000 * 20, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 86400000 * 4 },
  { content: '我和老婆是大学同学', scope: 'fact', ts: Date.now() - 86400000 * 170, confidence: 0.93, recallCount: 5, lastAccessed: Date.now() - 86400000 * 15 },
  { content: '我的 MacBook 是 M2 Pro 32G', scope: 'fact', ts: Date.now() - 86400000 * 45, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - 86400000 * 6 },
  { content: '我每周五和朋友打羽毛球', scope: 'fact', ts: Date.now() - 86400000 * 30, confidence: 0.83, recallCount: 4, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '我最近在看《三体》', scope: 'fact', ts: Date.now() - 86400000 * 10, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '去年做了近视手术', scope: 'fact', ts: Date.now() - 86400000 * 100, confidence: 0.9, recallCount: 1, lastAccessed: Date.now() - 86400000 * 40 },
  { content: '我在字节做安全工程师', scope: 'fact', ts: Date.now() - 86400000 * 12, confidence: 0.92, recallCount: 6, lastAccessed: Date.now() - 86400000 * 1 },

  // ── 40-79: New batch — social media, music, cooking, weather, childhood, goals, routines, shopping, transport, news ──
  // Social media / online habits (40-43)
  { content: '我每天刷抖音至少两小时', scope: 'fact', ts: Date.now() - 86400000 * 20, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '我有一个技术博客，写了 50 多篇文章', scope: 'fact', ts: Date.now() - 86400000 * 90, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - 86400000 * 10 },
  { content: '我微信好友有 2000 多人', scope: 'fact', ts: Date.now() - 86400000 * 60, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 86400000 * 15 },
  { content: '我在小红书上关注了很多美食博主', scope: 'fact', ts: Date.now() - 86400000 * 30, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 5 },

  // Music preferences (44-47)
  { content: '我最喜欢周杰伦的歌，听了二十年了', scope: 'preference', ts: Date.now() - 86400000 * 200, confidence: 0.92, recallCount: 5, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '写代码的时候习惯听 lo-fi 电子乐', scope: 'fact', ts: Date.now() - 86400000 * 40, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '上个月去看了五月天的演唱会', scope: 'episode', ts: Date.now() - 86400000 * 28, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - 86400000 * 7 },
  { content: '我小时候学过两年小提琴，后来没坚持', scope: 'fact', ts: Date.now() - 86400000 * 250, confidence: 0.83, recallCount: 1, lastAccessed: Date.now() - 86400000 * 30 },

  // Cooking skills (48-51)
  { content: '我会做糖醋排骨，是我的拿手菜', scope: 'fact', ts: Date.now() - 86400000 * 50, confidence: 0.9, recallCount: 4, lastAccessed: Date.now() - 86400000 * 8 },
  { content: '我做饭基本靠下厨房 App 看菜谱', scope: 'fact', ts: Date.now() - 86400000 * 35, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '上周学会了做提拉米苏', scope: 'episode', ts: Date.now() - 86400000 * 6, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '我不吃香菜，闻到就恶心', scope: 'preference', ts: Date.now() - 86400000 * 300, confidence: 0.95, recallCount: 4, lastAccessed: Date.now() - 86400000 * 10 },

  // Weather / seasonal preferences (52-55)
  { content: '我怕冷，冬天不愿意出门', scope: 'fact', ts: Date.now() - 86400000 * 120, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 86400000 * 15 },
  { content: '最喜欢秋天，不冷不热刚刚好', scope: 'preference', ts: Date.now() - 86400000 * 150, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 20 },
  { content: '下雨天就想在家打游戏', scope: 'fact', ts: Date.now() - 86400000 * 25, confidence: 0.8, recallCount: 3, lastAccessed: Date.now() - 86400000 * 4 },
  { content: '去年夏天中暑过一次，在公司晕倒了', scope: 'episode', ts: Date.now() - 86400000 * 80, confidence: 0.87, recallCount: 2, lastAccessed: Date.now() - 86400000 * 25 },

  // Childhood memories (56-59)
  { content: '小时候在农村长大，经常下河摸鱼', scope: 'fact', ts: Date.now() - 86400000 * 365, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - 86400000 * 40 },
  { content: '我小学的时候数学竞赛拿过市一等奖', scope: 'fact', ts: Date.now() - 86400000 * 350, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - 86400000 * 50 },
  { content: '我从小就怕打针，到现在还是', scope: 'fact', ts: Date.now() - 86400000 * 280, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 35 },
  { content: '小时候养过一条狗叫旺财，被车撞死了', scope: 'episode', ts: Date.now() - 86400000 * 400, confidence: 0.82, recallCount: 1, lastAccessed: Date.now() - 86400000 * 60 },

  // Future goals / dreams (60-63)
  { content: '我的梦想是开一家咖啡店', scope: 'fact', ts: Date.now() - 86400000 * 70, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 86400000 * 12 },
  { content: '计划明年考 PMP 项目管理证书', scope: 'fact', ts: Date.now() - 86400000 * 15, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '想在 35 岁之前攒够 200 万', scope: 'fact', ts: Date.now() - 86400000 * 45, confidence: 0.78, recallCount: 1, lastAccessed: Date.now() - 86400000 * 10 },
  { content: '打算三年内在老家给父母盖一栋新房子', scope: 'fact', ts: Date.now() - 86400000 * 55, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 86400000 * 8 },

  // Daily routines (64-67)
  { content: '我早上先喝咖啡再吃早饭', scope: 'fact', ts: Date.now() - 86400000 * 30, confidence: 0.88, recallCount: 4, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '中午一般在公司食堂吃饭', scope: 'fact', ts: Date.now() - 86400000 * 40, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '晚上洗完澡会看半小时 B 站', scope: 'fact', ts: Date.now() - 86400000 * 22, confidence: 0.82, recallCount: 3, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '睡前必须刷十分钟微博才能入睡', scope: 'fact', ts: Date.now() - 86400000 * 18, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 86400000 * 1 },

  // Shopping habits (68-71)
  { content: '每个月花在网购上大概 3000', scope: 'fact', ts: Date.now() - 86400000 * 35, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '双十一囤了一堆零食和日用品', scope: 'episode', ts: Date.now() - 86400000 * 140, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 86400000 * 20 },
  { content: '买衣服只在优衣库和 Zara 买', scope: 'preference', ts: Date.now() - 86400000 * 80, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 86400000 * 10 },
  { content: '最近迷上了买盲盒，已经花了一千多', scope: 'fact', ts: Date.now() - 86400000 * 10, confidence: 0.78, recallCount: 2, lastAccessed: Date.now() - 86400000 * 3 },

  // Transportation (72-75)
  { content: '我坐地铁上班，2 号线转 10 号线', scope: 'fact', ts: Date.now() - 86400000 * 50, confidence: 0.9, recallCount: 5, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '上班单程需要一个半小时', scope: 'fact', ts: Date.now() - 86400000 * 48, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '偶尔骑共享单车去地铁站', scope: 'fact', ts: Date.now() - 86400000 * 30, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '去年拿到驾照了但不太敢开车', scope: 'fact', ts: Date.now() - 86400000 * 100, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 15 },

  // News / current events interests (76-79)
  { content: '我关注科技新闻，每天看 36kr', scope: 'fact', ts: Date.now() - 86400000 * 60, confidence: 0.87, recallCount: 4, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '最近一直在关注 AI 大模型的发展', scope: 'fact', ts: Date.now() - 86400000 * 10, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '不看娱乐八卦，觉得浪费时间', scope: 'preference', ts: Date.now() - 86400000 * 90, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 12 },
  { content: '喜欢看 B 站的科普视频，关注了半佛仙人', scope: 'preference', ts: Date.now() - 86400000 * 55, confidence: 0.84, recallCount: 3, lastAccessed: Date.now() - 86400000 * 4 },

  // ── 80-99: Work details (项目/技术栈/同事/评价) ──
  { content: '我负责字节内部的风控系统，日均处理 2 亿条请求', scope: 'fact', ts: Date.now() - 86400000 * 20, confidence: 0.9, recallCount: 4, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '我们组用的技术栈是 Go + gRPC + Kafka + ClickHouse', scope: 'fact', ts: Date.now() - 86400000 * 25, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '我的直属 leader 叫王磊，人很 nice 但要求很高', scope: 'fact', ts: Date.now() - 86400000 * 40, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '上个季度绩效评 B+，差一点拿 A', scope: 'fact', ts: Date.now() - 86400000 * 15, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '同事李晨跟我关系最好，经常一起吃午饭', scope: 'fact', ts: Date.now() - 86400000 * 35, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '公司给配了两块 4K 显示器，办公体验很好', scope: 'fact', ts: Date.now() - 86400000 * 50, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 86400000 * 10 },
  { content: '我之前在美团干了两年，做外卖配送算法', scope: 'fact', ts: Date.now() - 86400000 * 200, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 86400000 * 20 },
  { content: '入职字节的时候年薪涨了 40%', scope: 'fact', ts: Date.now() - 86400000 * 180, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 15 },
  { content: '我们每两周一次 sprint review，组会用飞书文档写周报', scope: 'fact', ts: Date.now() - 86400000 * 30, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 4 },
  { content: '最近在做一个反欺诈模型的 POC，用的 Python + XGBoost', scope: 'fact', ts: Date.now() - 86400000 * 5, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '实习的时候在百度做过搜索推荐', scope: 'fact', ts: Date.now() - 86400000 * 300, confidence: 0.83, recallCount: 1, lastAccessed: Date.now() - 86400000 * 40 },
  { content: '公司楼下有个星巴克，我每天下午都去买一杯', scope: 'fact', ts: Date.now() - 86400000 * 20, confidence: 0.8, recallCount: 3, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '字节的工位是开放式的，噪音很大戴降噪耳机', scope: 'fact', ts: Date.now() - 86400000 * 45, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '上个月提了一个架构优化方案被 CTO 表扬了', scope: 'episode', ts: Date.now() - 86400000 * 28, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 7 },
  { content: '同事小陈刚离职去了快手，我有点动摇', scope: 'episode', ts: Date.now() - 86400000 * 8, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '年底可能会有一次晋升评审，我在准备述职 PPT', scope: 'fact', ts: Date.now() - 86400000 * 3, confidence: 0.82, recallCount: 1, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '我有 3 年 Go 经验、2 年 Python 经验、1 年 Rust 经验', scope: 'fact', ts: Date.now() - 86400000 * 10, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '字节的福利包括免费三餐、健身房、每年体检', scope: 'fact', ts: Date.now() - 86400000 * 60, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 15 },
  { content: '我的 GitHub 有 1200 个 star 的开源项目', scope: 'fact', ts: Date.now() - 86400000 * 80, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 86400000 * 8 },
  { content: '公司年会抽奖抽到了一台 iPad Pro', scope: 'episode', ts: Date.now() - 86400000 * 120, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 86400000 * 30 },

  // ── 100-119: Family details (父母/兄弟姐妹/家庭事件) ──
  { content: '我爸是中学数学老师，教了三十年书', scope: 'fact', ts: Date.now() - 86400000 * 300, confidence: 0.92, recallCount: 3, lastAccessed: Date.now() - 86400000 * 20 },
  { content: '我妈在超市当收银员，快退休了', scope: 'fact', ts: Date.now() - 86400000 * 280, confidence: 0.9, recallCount: 2, lastAccessed: Date.now() - 86400000 * 25 },
  { content: '我有个妹妹叫小敏，比我小四岁，在深圳做设计', scope: 'fact', ts: Date.now() - 86400000 * 250, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - 86400000 * 15 },
  { content: '妹妹去年结婚了，嫁给了她大学同学', scope: 'episode', ts: Date.now() - 86400000 * 150, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 30 },
  { content: '爷爷去年过世了，享年 85 岁', scope: 'episode', ts: Date.now() - 86400000 * 200, confidence: 0.9, recallCount: 2, lastAccessed: Date.now() - 86400000 * 40 },
  { content: '奶奶身体还好，自己一个人住在老家', scope: 'fact', ts: Date.now() - 86400000 * 180, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 30 },
  { content: '过年全家人都回长沙老家团聚，一般初三才散', scope: 'fact', ts: Date.now() - 86400000 * 100, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 86400000 * 60 },
  { content: '我爸高血压吃了十几年药了', scope: 'fact', ts: Date.now() - 86400000 * 150, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 20 },
  { content: '小雨的父母在杭州，每次去杭州都住她家', scope: 'fact', ts: Date.now() - 86400000 * 90, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 15 },
  { content: '家里的房子是 2020 年买的，在北京昌平回龙观', scope: 'fact', ts: Date.now() - 86400000 * 160, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - 86400000 * 10 },
  { content: '我叔叔在长沙开了一家湘菜馆，生意不错', scope: 'fact', ts: Date.now() - 86400000 * 200, confidence: 0.82, recallCount: 1, lastAccessed: Date.now() - 86400000 * 35 },
  { content: '我表哥在部队当兵，是个连长', scope: 'fact', ts: Date.now() - 86400000 * 220, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 86400000 * 50 },
  { content: '我妈经常催我赶紧结婚，每次打电话都提', scope: 'fact', ts: Date.now() - 86400000 * 30, confidence: 0.85, recallCount: 4, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '小雨和我妈关系不错，过年给她买了条金项链', scope: 'fact', ts: Date.now() - 86400000 * 70, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - 86400000 * 10 },
  { content: '我弟（表弟）今年高考，目标是 985', scope: 'fact', ts: Date.now() - 86400000 * 10, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '每年清明节回老家给爷爷扫墓', scope: 'fact', ts: Date.now() - 86400000 * 50, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 86400000 * 20 },
  { content: '家里养了一条金鱼和一盆绿萝，都是小雨在打理', scope: 'fact', ts: Date.now() - 86400000 * 40, confidence: 0.78, recallCount: 1, lastAccessed: Date.now() - 86400000 * 8 },
  { content: '我爸退休后迷上了钓鱼，每周去三次', scope: 'fact', ts: Date.now() - 86400000 * 15, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '妹妹刚怀孕两个月，我爸妈高兴坏了', scope: 'episode', ts: Date.now() - 86400000 * 5, confidence: 0.85, recallCount: 1, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '我和小雨打算明年领证，婚礼从简', scope: 'fact', ts: Date.now() - 86400000 * 8, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 86400000 * 2 },

  // ── 120-139: Health / Finance / Education ──
  { content: '我有慢性胃炎，不能喝酒不能吃辣（但还是偷偷吃）', scope: 'fact', ts: Date.now() - 86400000 * 100, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 86400000 * 10 },
  { content: '每半年去医院做一次胃镜检查', scope: 'fact', ts: Date.now() - 86400000 * 60, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 15 },
  { content: '医生给开了奥美拉唑和莫沙必利，每天饭前吃', scope: 'fact', ts: Date.now() - 86400000 * 50, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 8 },
  { content: '去年体检发现甲状腺结节，医生说定期复查就行', scope: 'fact', ts: Date.now() - 86400000 * 120, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 20 },
  { content: '我有腰椎间盘突出，坐久了就疼', scope: 'fact', ts: Date.now() - 86400000 * 80, confidence: 0.87, recallCount: 3, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '买了一把 Herman Miller 人体工学椅，花了八千多', scope: 'fact', ts: Date.now() - 86400000 * 70, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 10 },
  { content: '在蚂蚁财富上买了 10 万的货币基金', scope: 'fact', ts: Date.now() - 86400000 * 90, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 12 },
  { content: '每月定投沪深 300 指数基金 3000 块', scope: 'fact', ts: Date.now() - 86400000 * 75, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - 86400000 * 8 },
  { content: '买了百万医疗险和重疾险，每年交 6000', scope: 'fact', ts: Date.now() - 86400000 * 110, confidence: 0.85, recallCount: 1, lastAccessed: Date.now() - 86400000 * 25 },
  { content: '去年退税退了 4800 块', scope: 'episode', ts: Date.now() - 86400000 * 130, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 86400000 * 30 },
  { content: '公积金每个月交 3200，打算以后提取出来还房贷', scope: 'fact', ts: Date.now() - 86400000 * 55, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 10 },
  { content: '武汉大学计算机学院，大三拿过国家奖学金', scope: 'fact', ts: Date.now() - 86400000 * 280, confidence: 0.9, recallCount: 2, lastAccessed: Date.now() - 86400000 * 35 },
  { content: '毕业设计做的是基于深度学习的人脸识别系统', scope: 'fact', ts: Date.now() - 86400000 * 260, confidence: 0.85, recallCount: 1, lastAccessed: Date.now() - 86400000 * 40 },
  { content: '大学的数据结构老师姓周，讲课特别好', scope: 'fact', ts: Date.now() - 86400000 * 270, confidence: 0.82, recallCount: 1, lastAccessed: Date.now() - 86400000 * 45 },
  { content: '考研考了两次，第一次差 3 分没过线', scope: 'fact', ts: Date.now() - 86400000 * 240, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 50 },
  { content: '后来放弃考研直接工作了，现在想想也不后悔', scope: 'fact', ts: Date.now() - 86400000 * 230, confidence: 0.82, recallCount: 1, lastAccessed: Date.now() - 86400000 * 45 },
  { content: '高中在长沙一中读的，班主任姓刘，对我影响很大', scope: 'fact', ts: Date.now() - 86400000 * 350, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - 86400000 * 55 },
  { content: '信用卡额度 5 万，一般用到一半左右', scope: 'fact', ts: Date.now() - 86400000 * 65, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 86400000 * 12 },
  { content: '在腾讯理财通还有 5 万定期存款', scope: 'fact', ts: Date.now() - 86400000 * 85, confidence: 0.83, recallCount: 1, lastAccessed: Date.now() - 86400000 * 15 },
  { content: '每个月到手工资大概 2.8 万', scope: 'fact', ts: Date.now() - 86400000 * 30, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 86400000 * 5 },

  // ── 140-159: Social / Hobbies / Daily routine details ──
  { content: '高中同学群里最活跃的是老赵，每天发段子', scope: 'fact', ts: Date.now() - 86400000 * 100, confidence: 0.78, recallCount: 1, lastAccessed: Date.now() - 86400000 * 15 },
  { content: '大学好哥们刘毅在深圳创业做 SaaS，经常找我聊技术', scope: 'fact', ts: Date.now() - 86400000 * 80, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 10 },
  { content: '每个月和大学同学线上打一次狼人杀', scope: 'fact', ts: Date.now() - 86400000 * 40, confidence: 0.82, recallCount: 3, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '我的邻居是一对退休夫妇，经常送我们自己种的菜', scope: 'fact', ts: Date.now() - 86400000 * 60, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 86400000 * 8 },
  { content: '去年参加了公司的黑客马拉松，拿了二等奖', scope: 'episode', ts: Date.now() - 86400000 * 140, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 20 },
  { content: '我在 LeetCode 上刷了 600 多道题', scope: 'fact', ts: Date.now() - 86400000 * 90, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - 86400000 * 10 },
  { content: '最近迷上了机械键盘，已经买了三把了', scope: 'fact', ts: Date.now() - 86400000 * 12, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '喜欢玩原神，雷电将军满命了', scope: 'fact', ts: Date.now() - 86400000 * 50, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 86400000 * 4 },
  { content: '每周日下午去楼下咖啡馆看书两小时', scope: 'fact', ts: Date.now() - 86400000 * 25, confidence: 0.82, recallCount: 3, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '早上 6:50 闹钟响，赖床十分钟', scope: 'fact', ts: Date.now() - 86400000 * 18, confidence: 0.85, recallCount: 4, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '从家走到地铁站要 15 分钟', scope: 'fact', ts: Date.now() - 86400000 * 35, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '午休一般趴在桌上睡半小时', scope: 'fact', ts: Date.now() - 86400000 * 28, confidence: 0.8, recallCount: 3, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '每天下午三点喝杯咖啡续命', scope: 'fact', ts: Date.now() - 86400000 * 22, confidence: 0.82, recallCount: 3, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '晚饭经常点外卖，最常点的是黄焖鸡', scope: 'fact', ts: Date.now() - 86400000 * 15, confidence: 0.8, recallCount: 3, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '洗完澡习惯用吹风机把头发完全吹干', scope: 'fact', ts: Date.now() - 86400000 * 20, confidence: 0.75, recallCount: 1, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '每天晚上十点半开始洗漱', scope: 'fact', ts: Date.now() - 86400000 * 16, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '健身房办了年卡但只去了五次', scope: 'fact', ts: Date.now() - 86400000 * 70, confidence: 0.78, recallCount: 1, lastAccessed: Date.now() - 86400000 * 15 },
  { content: '我喜欢拍照，手机里有 2 万多张照片', scope: 'fact', ts: Date.now() - 86400000 * 55, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '最近在用 Notion 做个人知识管理', scope: 'fact', ts: Date.now() - 86400000 * 8, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '每周三晚上和小雨一起看综艺', scope: 'fact', ts: Date.now() - 86400000 * 20, confidence: 0.82, recallCount: 3, lastAccessed: Date.now() - 86400000 * 3 },

  // ── 160-179: Personality / Life events / Travel ──
  { content: '我脾气比较急，说话直来直去容易得罪人', scope: 'fact', ts: Date.now() - 86400000 * 150, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 86400000 * 10 },
  { content: '遇到不公平的事情会当面说出来，不会憋着', scope: 'fact', ts: Date.now() - 86400000 * 130, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 12 },
  { content: '决定买什么东西之前会做大量功课，看测评对比', scope: 'fact', ts: Date.now() - 86400000 * 80, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '不太喜欢社交场合，聚会超过十个人就不自在', scope: 'preference', ts: Date.now() - 86400000 * 120, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 15 },
  { content: '做事喜欢列清单，每天用滴答清单管理任务', scope: 'fact', ts: Date.now() - 86400000 * 45, confidence: 0.83, recallCount: 3, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '压力大的时候喜欢一个人去江边走走', scope: 'fact', ts: Date.now() - 86400000 * 60, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 8 },
  { content: '2022 年从上海搬到了北京，因为字节的 offer', scope: 'episode', ts: Date.now() - 86400000 * 250, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - 86400000 * 20 },
  { content: '在上海的时候住在浦东张江，离公司很近', scope: 'fact', ts: Date.now() - 86400000 * 280, confidence: 0.83, recallCount: 1, lastAccessed: Date.now() - 86400000 * 30 },
  { content: '去年国庆去了西安，看了兵马俑和大唐不夜城', scope: 'episode', ts: Date.now() - 86400000 * 160, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 25 },
  { content: '蜜月计划去马尔代夫，已经在看攻略了', scope: 'fact', ts: Date.now() - 86400000 * 6, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '大学的时候一个人背包去了云南，住了半个月', scope: 'episode', ts: Date.now() - 86400000 * 300, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 40 },
  { content: '出差去过深圳、广州、成都，最喜欢成都', scope: 'fact', ts: Date.now() - 86400000 * 100, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 20 },
  { content: '有选择困难症，点外卖能纠结十分钟', scope: 'fact', ts: Date.now() - 86400000 * 50, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '我习惯把手机调成静音，经常漏接电话', scope: 'fact', ts: Date.now() - 86400000 * 35, confidence: 0.78, recallCount: 2, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '不喜欢麻烦别人，能自己搞定的绝不求人', scope: 'preference', ts: Date.now() - 86400000 * 110, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 10 },
  { content: '情绪不好的时候会暴饮暴食', scope: 'fact', ts: Date.now() - 86400000 * 70, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 86400000 * 8 },
  { content: '前年学了潜水，考了 PADI OW 证', scope: 'fact', ts: Date.now() - 86400000 * 200, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 25 },
  { content: '今年生日收到了一块小雨送的 Apple Watch', scope: 'episode', ts: Date.now() - 86400000 * 40, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '和前女友分手是因为异地恋撑不下去了', scope: 'fact', ts: Date.now() - 86400000 * 350, confidence: 0.82, recallCount: 1, lastAccessed: Date.now() - 86400000 * 50 },
  { content: '第一份工作是在美团实习转正的', scope: 'fact', ts: Date.now() - 86400000 * 290, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 35 },

  // ── 180-199: More specific details ──
  { content: '手机用的是 iPhone 15 Pro Max，之前一直用安卓', scope: 'fact', ts: Date.now() - 86400000 * 30, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '最讨厌被问"你什么时候结婚"', scope: 'preference', ts: Date.now() - 86400000 * 40, confidence: 0.82, recallCount: 3, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '我用 Spotify 听歌，不用网易云因为版权少', scope: 'preference', ts: Date.now() - 86400000 * 25, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '喜欢喝美式咖啡，不加糖不加奶', scope: 'preference', ts: Date.now() - 86400000 * 50, confidence: 0.88, recallCount: 4, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '有一副 AirPods Pro，通勤时戴着听播客', scope: 'fact', ts: Date.now() - 86400000 * 35, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '最近在听一个叫《硬地骇客》的技术播客', scope: 'fact', ts: Date.now() - 86400000 * 10, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '每年 618 和双十一会屯一批书', scope: 'fact', ts: Date.now() - 86400000 * 45, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 86400000 * 10 },
  { content: '最近想学摄影，看中了一台富士 X-T5', scope: 'fact', ts: Date.now() - 86400000 * 4, confidence: 0.78, recallCount: 1, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '上次搬家扔了十几箱旧书和衣服', scope: 'episode', ts: Date.now() - 86400000 * 250, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 86400000 * 30 },
  { content: '我有一双 Nike 跑鞋和一双 Adidas 篮球鞋', scope: 'fact', ts: Date.now() - 86400000 * 55, confidence: 0.78, recallCount: 1, lastAccessed: Date.now() - 86400000 * 8 },
  { content: '睡觉必须开空调，不管冬天夏天', scope: 'fact', ts: Date.now() - 86400000 * 60, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 3 },
  { content: '用 Chrome 浏览器，装了十几个扩展', scope: 'fact', ts: Date.now() - 86400000 * 40, confidence: 0.78, recallCount: 1, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '有强迫症倾向，出门总是反复确认锁没锁门', scope: 'fact', ts: Date.now() - 86400000 * 75, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - 86400000 * 6 },
  { content: '做菜喜欢放很多蒜，小雨嫌味道大', scope: 'fact', ts: Date.now() - 86400000 * 30, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 86400000 * 4 },
  { content: '每周和爸妈视频通话两次，一般周三和周日', scope: 'fact', ts: Date.now() - 86400000 * 20, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 86400000 * 2 },
  { content: '公司有个读书会，我推荐了《黑客与画家》', scope: 'fact', ts: Date.now() - 86400000 * 18, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 86400000 * 5 },
  { content: '夏天喜欢穿拖鞋短裤，冬天全靠羽绒服', scope: 'fact', ts: Date.now() - 86400000 * 100, confidence: 0.78, recallCount: 1, lastAccessed: Date.now() - 86400000 * 20 },
  { content: '口腔溃疡反复发作，医生说缺维生素 B', scope: 'fact', ts: Date.now() - 86400000 * 15, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 86400000 * 4 },
  { content: '最近在研究 Home Assistant 搞智能家居', scope: 'fact', ts: Date.now() - 86400000 * 7, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 86400000 * 1 },
  { content: '周末偶尔和小雨一起去宜家逛街', scope: 'fact', ts: Date.now() - 86400000 * 22, confidence: 0.78, recallCount: 2, lastAccessed: Date.now() - 86400000 * 4 },
] as Memory[]

// ═══════════════════════════════════════════════════════════════
// TEST QUERIES: 520 queries (220 direct + 200 semantic + 100 hard)
// ═══════════════════════════════════════════════════════════════

interface TestCase {
  query: string
  expectedIndex: number | number[]  // single index or array (multi-match: pass if ANY hit)
  type: 'direct' | 'semantic' | 'hard'
  description: string
}

const TEST_CASES: TestCase[] = [
  // ════════════════════════════════════════════════════════════
  // DIRECT QUERIES (100 total)
  // ════════════════════════════════════════════════════════════

  // Memory 0-19: Original direct
  { query: '你在哪里上班', expectedIndex: 0, type: 'direct', description: '工作→字节' },
  { query: '你女朋友叫什么', expectedIndex: 1, type: 'direct', description: '女朋友→小雨' },
  { query: '你血压怎么样', expectedIndex: 2, type: 'direct', description: '血压→高' },
  { query: '你养了什么宠物', expectedIndex: 3, type: 'direct', description: '宠物→橘猫' },
  { query: '你在哪里上的大学', expectedIndex: 4, type: 'direct', description: '大学→武汉' },
  { query: '你去过成都吗', expectedIndex: 5, type: 'direct', description: '成都→旅游' },
  { query: '你每天跑多少公里', expectedIndex: 6, type: 'direct', description: '跑步→5公里' },
  { query: '你在学什么新技术', expectedIndex: 7, type: 'direct', description: '技术→Rust' },
  { query: '你妈做什么菜好吃', expectedIndex: 8, type: 'direct', description: '妈→红烧肉' },
  { query: '你面试阿里怎么样了', expectedIndex: 9, type: 'direct', description: '面试→阿里' },
  { query: '你睡眠怎么样', expectedIndex: 10, type: 'direct', description: '睡眠→失眠' },
  { query: '你每个月还多少房贷', expectedIndex: 11, type: 'direct', description: '房贷→8000' },
  { query: '小雨预产期是什么时候', expectedIndex: 12, type: 'direct', description: '预产期→三月' },
  { query: '你喜欢看什么电影', expectedIndex: 13, type: 'direct', description: '电影→科幻' },
  { query: '你周末打篮球吗', expectedIndex: 14, type: 'direct', description: '篮球→周末' },
  { query: '你对什么过敏', expectedIndex: 15, type: 'direct', description: '过敏→花粉' },
  { query: '你想买什么车', expectedIndex: 16, type: 'direct', description: '买车→特斯拉' },
  { query: '你老家在哪里', expectedIndex: 17, type: 'direct', description: '老家→长沙' },
  { query: '你下个月有什么安排', expectedIndex: 18, type: 'direct', description: '安排→婚礼' },
  { query: '你最近加班多吗', expectedIndex: 19, type: 'direct', description: '加班→十一点' },

  // Memory 20-39: Second batch direct
  { query: '我几点起床', expectedIndex: 20, type: 'direct', description: '起床→7点跑步' },
  { query: '我对什么过敏', expectedIndex: 21, type: 'direct', description: '过敏→花粉' },
  { query: '我开什么车', expectedIndex: 22, type: 'direct', description: '开车→特斯拉' },
  { query: '我工资涨了多少', expectedIndex: 23, type: 'direct', description: '涨薪→2000' },
  { query: '我女儿学什么乐器', expectedIndex: 24, type: 'direct', description: '乐器→钢琴' },
  { query: '我戒烟多久了', expectedIndex: 25, type: 'direct', description: '戒烟→47天' },
  { query: '我怕什么', expectedIndex: 26, type: 'direct', description: '怕→蛇' },
  { query: '我下个月去哪旅游', expectedIndex: 27, type: 'direct', description: '旅游→日本' },
  { query: '我室友叫什么', expectedIndex: 28, type: 'direct', description: '室友→张磊' },
  { query: '我什么血型', expectedIndex: 29, type: 'direct', description: '血型→O型' },
  { query: '周末一般干嘛', expectedIndex: 30, type: 'direct', description: '周末→陪孩子公园' },
  { query: '我想去哪个公司', expectedIndex: 31, type: 'direct', description: '公司→阿里' },
  { query: '我炒股亏了多少', expectedIndex: 32, type: 'direct', description: '炒股→3万' },
  { query: '我在学什么语言', expectedIndex: 33, type: 'direct', description: '学语言→日语' },
  { query: '我老婆怎么认识的', expectedIndex: 34, type: 'direct', description: '老婆→大学同学' },
  { query: '我电脑什么配置', expectedIndex: 35, type: 'direct', description: '电脑→M2 Pro' },
  { query: '我周五做什么运动', expectedIndex: 36, type: 'direct', description: '周五运动→羽毛球' },
  { query: '我最近在看什么书', expectedIndex: 37, type: 'direct', description: '看书→三体' },
  { query: '我做过什么手术', expectedIndex: 38, type: 'direct', description: '手术→近视' },
  { query: '我在哪工作', expectedIndex: 39, type: 'direct', description: '工作→字节安全' },

  // Memory 40-43: Social media direct
  { query: '我每天刷抖音多久', expectedIndex: 40, type: 'direct', description: '抖音→两小时' },
  { query: '我有技术博客吗', expectedIndex: 41, type: 'direct', description: '博客→50篇' },
  { query: '我微信有多少好友', expectedIndex: 42, type: 'direct', description: '微信→2000人' },
  { query: '我在小红书上关注什么', expectedIndex: 43, type: 'direct', description: '小红书→美食博主' },

  // Memory 44-47: Music direct
  { query: '我最喜欢谁的歌', expectedIndex: 44, type: 'direct', description: '喜欢歌→周杰伦' },
  { query: '写代码时听什么音乐', expectedIndex: 45, type: 'direct', description: '代码音乐→lo-fi' },
  { query: '我去看过什么演唱会', expectedIndex: 46, type: 'direct', description: '演唱会→五月天' },
  { query: '我小时候学过什么乐器', expectedIndex: 47, type: 'direct', description: '乐器→小提琴' },

  // Memory 48-51: Cooking direct
  { query: '我的拿手菜是什么', expectedIndex: 48, type: 'direct', description: '拿手菜→糖醋排骨' },
  { query: '我用什么 App 看菜谱', expectedIndex: 49, type: 'direct', description: '菜谱→下厨房' },
  { query: '我最近学会做什么甜品', expectedIndex: 50, type: 'direct', description: '甜品→提拉米苏' },
  { query: '我不吃什么菜', expectedIndex: 51, type: 'direct', description: '不吃→香菜' },

  // Memory 52-55: Weather direct
  { query: '你怕冷吗', expectedIndex: 52, type: 'direct', description: '怕冷→冬天不出门' },
  { query: '你最喜欢什么季节', expectedIndex: 53, type: 'direct', description: '季节→秋天' },
  { query: '下雨天你一般干嘛', expectedIndex: 54, type: 'direct', description: '下雨→打游戏' },
  { query: '你中暑过吗', expectedIndex: 55, type: 'direct', description: '中暑→公司晕倒' },

  // Memory 56-59: Childhood direct
  { query: '你小时候在哪里长大', expectedIndex: 56, type: 'direct', description: '小时候→农村' },
  { query: '你数学成绩好吗', expectedIndex: 57, type: 'direct', description: '数学→竞赛一等奖' },
  { query: '你怕打针吗', expectedIndex: 58, type: 'direct', description: '打针→怕' },
  { query: '你小时候养过什么动物', expectedIndex: 59, type: 'direct', description: '动物→狗旺财' },

  // Memory 60-63: Goals direct
  { query: '你的梦想是什么', expectedIndex: 60, type: 'direct', description: '梦想→咖啡店' },
  { query: '你打算考什么证', expectedIndex: 61, type: 'direct', description: '考证→PMP' },
  { query: '你想攒多少钱', expectedIndex: 62, type: 'direct', description: '攒钱→200万' },
  { query: '你给父母有什么打算', expectedIndex: 63, type: 'direct', description: '父母→盖房子' },

  // Memory 64-67: Routines direct
  { query: '你早上先干嘛', expectedIndex: 64, type: 'direct', description: '早上→喝咖啡' },
  { query: '你中午在哪吃饭', expectedIndex: 65, type: 'direct', description: '中午→食堂' },
  { query: '你晚上洗完澡干嘛', expectedIndex: 66, type: 'direct', description: '洗澡后→B站' },
  { query: '你睡前做什么', expectedIndex: 67, type: 'direct', description: '睡前→刷微博' },

  // Memory 68-71: Shopping direct
  { query: '你每个月网购花多少钱', expectedIndex: 68, type: 'direct', description: '网购→3000' },
  { query: '你双十一买了什么', expectedIndex: 69, type: 'direct', description: '双十一→零食日用品' },
  { query: '你在哪买衣服', expectedIndex: 70, type: 'direct', description: '买衣服→优衣库Zara' },
  { query: '你买盲盒花了多少', expectedIndex: 71, type: 'direct', description: '盲盒→一千多' },

  // Memory 72-75: Transport direct
  { query: '你怎么上班', expectedIndex: 72, type: 'direct', description: '上班→地铁2转10' },
  { query: '你上班路上要多久', expectedIndex: 73, type: 'direct', description: '通勤→一个半小时' },
  { query: '你骑共享单车吗', expectedIndex: 74, type: 'direct', description: '单车→去地铁站' },
  { query: '你有驾照吗', expectedIndex: 75, type: 'direct', description: '驾照→有但不敢开' },

  // Memory 76-79: News direct
  { query: '你看什么新闻', expectedIndex: 76, type: 'direct', description: '新闻→36kr科技' },
  { query: '你关注 AI 吗', expectedIndex: 77, type: 'direct', description: 'AI→大模型' },
  { query: '你看娱乐八卦吗', expectedIndex: 78, type: 'direct', description: '八卦→不看' },
  { query: '你在 B 站关注了谁', expectedIndex: 79, type: 'direct', description: 'B站→半佛仙人' },

  // ════════════════════════════════════════════════════════════
  // SEMANTIC QUERIES (100 total)
  // ════════════════════════════════════════════════════════════

  // Memory 0-19: Original semantic
  { query: '你会什么编程语言', expectedIndex: 0, type: 'semantic', description: '编程语言→Go' },
  { query: '你对象是谁', expectedIndex: 1, type: 'semantic', description: '对象→女朋友' },
  { query: '你有什么健康问题', expectedIndex: 2, type: 'semantic', description: '健康→血压' },
  { query: '橘子最近怎么样', expectedIndex: 3, type: 'semantic', description: '橘子→猫名' },
  { query: '你母校在哪', expectedIndex: 4, type: 'semantic', description: '母校→大学' },
  { query: '你喜欢吃什么美食', expectedIndex: 5, type: 'semantic', description: '美食→火锅' },
  { query: '你有什么锻炼习惯', expectedIndex: 6, type: 'semantic', description: '锻炼→跑步' },
  { query: '所有权系统你搞懂了吗', expectedIndex: 7, type: 'semantic', description: '所有权→Rust' },
  { query: '你回家最想吃什么', expectedIndex: 8, type: 'semantic', description: '回家吃→红烧肉' },
  { query: '你最近有没有找工作', expectedIndex: 9, type: 'semantic', description: '找工作→面试' },
  { query: '你几点睡觉', expectedIndex: 10, type: 'semantic', description: '几点睡→凌晨一点' },
  { query: '你有什么经济压力', expectedIndex: 11, type: 'semantic', description: '经济压力→房贷' },
  { query: '你要当爸爸了吗', expectedIndex: 12, type: 'semantic', description: '当爸爸→怀孕' },
  { query: '星际穿越你看过吗', expectedIndex: 13, type: 'semantic', description: '星际穿越→最喜欢' },
  { query: '你有什么运动爱好', expectedIndex: 14, type: 'semantic', description: '运动爱好→篮球' },
  { query: '春天出门你要注意什么', expectedIndex: 15, type: 'semantic', description: '春天注意→口罩' },
  { query: '你考虑入手电动车吗', expectedIndex: 16, type: 'semantic', description: '电动车→特斯拉' },
  { query: '你能吃辣吗', expectedIndex: 17, type: 'semantic', description: '吃辣→湖南' },
  { query: '份子钱准备了多少', expectedIndex: 18, type: 'semantic', description: '份子钱→婚礼' },
  { query: '你工作累不累', expectedIndex: 19, type: 'semantic', description: '工作累→加班' },

  // Memory 20-39: Second batch semantic
  { query: '我的晨练习惯', expectedIndex: 20, type: 'semantic', description: '晨练→跑步' },
  { query: '我有什么健康隐患', expectedIndex: [21, 38], type: 'semantic', description: '健康隐患→过敏/近视' },
  { query: '我的交通工具', expectedIndex: 22, type: 'semantic', description: '交通工具→特斯拉' },
  { query: '我的收入变化', expectedIndex: 23, type: 'semantic', description: '收入变化→涨薪' },
  { query: '孩子的课外活动', expectedIndex: 24, type: 'semantic', description: '课外活动→钢琴' },
  { query: '我在克服什么坏习惯', expectedIndex: 25, type: 'semantic', description: '坏习惯→戒烟' },
  { query: '我的恐惧', expectedIndex: 26, type: 'semantic', description: '恐惧→蛇' },
  { query: '最近的旅行计划', expectedIndex: 27, type: 'semantic', description: '旅行计划→日本' },
  { query: '我的老同学现在干嘛', expectedIndex: 28, type: 'semantic', description: '老同学→张磊腾讯' },
  { query: '我的职业规划', expectedIndex: 31, type: 'semantic', description: '职业规划→换工作阿里' },
  { query: '我的投资情况', expectedIndex: 32, type: 'semantic', description: '投资→炒股亏3万' },
  { query: '我在自我提升什么', expectedIndex: 33, type: 'semantic', description: '自我提升→学日语' },
  { query: '我和老婆的故事', expectedIndex: 34, type: 'semantic', description: '老婆故事→大学同学' },
  { query: '我的数码装备', expectedIndex: 35, type: 'semantic', description: '数码装备→MacBook' },
  { query: '我的运动习惯', expectedIndex: [20, 36], type: 'semantic', description: '运动→跑步/羽毛球' },
  { query: '我的阅读偏好', expectedIndex: 37, type: 'semantic', description: '阅读→三体' },
  { query: '我的视力情况', expectedIndex: 38, type: 'semantic', description: '视力→近视手术' },
  { query: '我家里几口人', expectedIndex: [24, 34], type: 'semantic', description: '家人→老婆+女儿' },
  { query: '我周末的安排', expectedIndex: 30, type: 'semantic', description: '周末安排→陪孩子公园' },
  { query: '我最近有什么烦心事', expectedIndex: [32, 31], type: 'semantic', description: '烦心事→亏钱/换工作' },

  // Memory 40-43: Social media semantic
  { query: '你平时玩什么短视频', expectedIndex: 40, type: 'semantic', description: '短视频→抖音' },
  { query: '你有没有在网上写东西', expectedIndex: 41, type: 'semantic', description: '写东西→技术博客' },
  { query: '你的社交圈大吗', expectedIndex: 42, type: 'semantic', description: '社交圈→微信2000人' },
  { query: '你平时怎么发现好吃的', expectedIndex: 43, type: 'semantic', description: '发现美食→小红书' },

  // Memory 44-47: Music semantic
  { query: '你的音乐品味', expectedIndex: 44, type: 'semantic', description: '音乐品味→周杰伦' },
  { query: '你工作时需要什么氛围', expectedIndex: 45, type: 'semantic', description: '工作氛围→lo-fi音乐' },
  { query: '你最近有什么娱乐活动', expectedIndex: 46, type: 'semantic', description: '娱乐活动→五月天演唱会' },
  { query: '你有什么半途而废的事', expectedIndex: 47, type: 'semantic', description: '半途而废→小提琴' },

  // Memory 48-51: Cooking semantic
  { query: '你厨艺怎么样', expectedIndex: 48, type: 'semantic', description: '厨艺→糖醋排骨' },
  { query: '你是怎么学做饭的', expectedIndex: 49, type: 'semantic', description: '学做饭→下厨房App' },
  { query: '你最近在厨房搞什么花样', expectedIndex: 50, type: 'semantic', description: '厨房花样→提拉米苏' },
  { query: '你有什么忌口', expectedIndex: 51, type: 'semantic', description: '忌口→香菜' },

  // Memory 52-55: Weather semantic
  { query: '你冬天一般宅在家吗', expectedIndex: 52, type: 'semantic', description: '冬天宅→怕冷' },
  { query: '什么天气让你最舒服', expectedIndex: 53, type: 'semantic', description: '舒服天气→秋天' },
  { query: '你平时打什么游戏', expectedIndex: 54, type: 'semantic', description: '游戏→下雨天' },
  { query: '你在公司出过什么状况', expectedIndex: 55, type: 'semantic', description: '公司状况→中暑晕倒' },

  // Memory 56-59: Childhood semantic
  { query: '你的童年是什么样的', expectedIndex: 56, type: 'semantic', description: '童年→农村摸鱼' },
  { query: '你从小学习就好吗', expectedIndex: 57, type: 'semantic', description: '学习好→数学竞赛' },
  { query: '你去医院会紧张吗', expectedIndex: 58, type: 'semantic', description: '医院紧张→怕打针' },
  { query: '你以前养过宠物吗', expectedIndex: 59, type: 'semantic', description: '以前宠物→旺财' },

  // Memory 60-63: Goals semantic
  { query: '你有什么创业想法', expectedIndex: 60, type: 'semantic', description: '创业→咖啡店' },
  { query: '你在规划什么职业发展', expectedIndex: 61, type: 'semantic', description: '职业发展→PMP' },
  { query: '你的财务目标', expectedIndex: 62, type: 'semantic', description: '财务目标→200万' },
  { query: '你对父母的孝心', expectedIndex: 63, type: 'semantic', description: '孝心→盖房' },

  // Memory 64-67: Routines semantic
  { query: '你有什么早起仪式', expectedIndex: 64, type: 'semantic', description: '早起仪式→咖啡' },
  { query: '你午餐怎么解决', expectedIndex: 65, type: 'semantic', description: '午餐→食堂' },
  { query: '你的睡前娱乐', expectedIndex: [66, 67], type: 'semantic', description: '睡前娱乐→B站/微博' },
  { query: '你有什么放松方式', expectedIndex: [66, 54], type: 'semantic', description: '放松→B站/游戏' },

  // Memory 68-71: Shopping semantic
  { query: '你消费水平怎么样', expectedIndex: 68, type: 'semantic', description: '消费水平→网购3000' },
  { query: '你囤货严重吗', expectedIndex: 69, type: 'semantic', description: '囤货→双十一' },
  { query: '你的穿衣风格', expectedIndex: 70, type: 'semantic', description: '穿衣→优衣库Zara' },
  { query: '你有什么烧钱的爱好', expectedIndex: 71, type: 'semantic', description: '烧钱爱好→盲盒' },

  // Memory 72-75: Transport semantic
  { query: '你的通勤方式', expectedIndex: 72, type: 'semantic', description: '通勤→地铁' },
  { query: '你每天花多少时间在路上', expectedIndex: 73, type: 'semantic', description: '路上时间→一个半小时' },
  { query: '最后一公里怎么解决', expectedIndex: 74, type: 'semantic', description: '最后一公里→共享单车' },
  { query: '你会开车吗', expectedIndex: 75, type: 'semantic', description: '开车→有驾照不敢开' },

  // Memory 76-79: News semantic
  { query: '你关注什么领域的资讯', expectedIndex: 76, type: 'semantic', description: '资讯→科技36kr' },
  { query: '你对 ChatGPT 怎么看', expectedIndex: 77, type: 'semantic', description: 'ChatGPT→关注AI大模型' },
  { query: '你对明星八卦感兴趣吗', expectedIndex: 78, type: 'semantic', description: '明星八卦→不看' },
  { query: '你用什么打发碎片时间', expectedIndex: [79, 40], type: 'semantic', description: '碎片时间→B站/抖音' },

  // ════════════════════════════════════════════════════════════
  // CROSS-DOMAIN / MULTI-MATCH / HARD QUERIES (20 extra, filling to 200)
  // ════════════════════════════════════════════════════════════

  // Multi-memory: daily routine composite
  { query: '我的日常作息是什么样的', expectedIndex: [20, 64, 65, 66, 67], type: 'semantic', description: '日常作息→起床+咖啡+食堂+B站+微博' },
  { query: '描述一下我的一天', expectedIndex: [20, 64, 72, 65, 66], type: 'semantic', description: '一天→起床+咖啡+地铁+食堂+B站' },

  // Negative / exclusion queries
  { query: '我有什么不喜欢吃的', expectedIndex: 51, type: 'semantic', description: '不喜欢吃→香菜' },
  { query: '我不擅长什么', expectedIndex: [75, 47], type: 'semantic', description: '不擅长→开车/小提琴' },

  // Temporal queries
  { query: '我最近在学什么新东西', expectedIndex: [7, 33], type: 'semantic', description: '学新东西→Rust+日语' },
  { query: '我最近花钱买了什么', expectedIndex: [71, 69], type: 'semantic', description: '最近花钱→盲盒/双十一' },

  // Abstract personality queries
  { query: '我的性格特点是什么', expectedIndex: [52, 26, 58], type: 'semantic', description: '性格→怕冷+怕蛇+怕打针' },
  { query: '我是一个怎样的人', expectedIndex: [0, 56, 60], type: 'semantic', description: '怎样的人→工作+童年+梦想' },

  // Cross-domain queries
  { query: '我在网上花多少时间', expectedIndex: [40, 66, 67], type: 'semantic', description: '网上时间→抖音+B站+微博' },
  { query: '我有哪些固定开支', expectedIndex: [11, 68], type: 'semantic', description: '固定开支→房贷+网购' },
  { query: '我都害怕什么', expectedIndex: [26, 58, 52], type: 'semantic', description: '害怕→蛇+打针+冷' },
  { query: '我的社交活动', expectedIndex: [14, 36, 46], type: 'semantic', description: '社交→篮球+羽毛球+演唱会' },
  { query: '我学过哪些技能', expectedIndex: [7, 33, 47], type: 'semantic', description: '技能→Rust+日语+小提琴' },
  { query: '我的饮食偏好', expectedIndex: [17, 51, 48], type: 'semantic', description: '饮食→吃辣+不吃香菜+糖醋排骨' },
  { query: '我有什么经济负担', expectedIndex: [11, 32, 68], type: 'semantic', description: '经济负担→房贷+亏钱+网购' },
  { query: '我对未来有什么规划', expectedIndex: [60, 61, 62, 63], type: 'semantic', description: '未来规划→咖啡店+PMP+攒钱+盖房' },
  { query: '我在字节做什么岗位', expectedIndex: [0, 39], type: 'direct', description: '字节岗位→后端/安全' },
  { query: '和小雨的关系进展', expectedIndex: [1, 12], type: 'direct', description: '小雨→在一起+怀孕' },
  { query: '我坐几号线地铁', expectedIndex: 72, type: 'direct', description: '几号线→2转10' },
  { query: '我在 36kr 上看什么', expectedIndex: 76, type: 'direct', description: '36kr→科技新闻' },

  // ── Additional direct queries to reach 100 ──
  { query: '我的抖音使用时间', expectedIndex: 40, type: 'direct', description: '抖音时间→两小时' },
  { query: '周杰伦的歌我听了多久', expectedIndex: 44, type: 'direct', description: '周杰伦→二十年' },
  { query: '糖醋排骨是我做的吗', expectedIndex: 48, type: 'direct', description: '糖醋排骨→拿手菜' },
  { query: '冬天我愿意出门吗', expectedIndex: 52, type: 'direct', description: '冬天出门→不愿意' },
  { query: '我小时候去河里干嘛', expectedIndex: 56, type: 'direct', description: '河里→摸鱼' },
  { query: '我想开什么店', expectedIndex: 60, type: 'direct', description: '开店→咖啡店' },
  { query: '我早饭前先干嘛', expectedIndex: 64, type: 'direct', description: '早饭前→喝咖啡' },
  { query: '我网购一般花多少', expectedIndex: 68, type: 'direct', description: '网购金额→3000' },
  { query: '我坐地铁转哪条线', expectedIndex: 72, type: 'direct', description: '转线→2转10' },
  { query: '我每天看 36kr 吗', expectedIndex: 76, type: 'direct', description: '36kr→每天看' },
  { query: '五月天的演唱会什么时候去的', expectedIndex: 46, type: 'direct', description: '五月天→上个月' },
  { query: '提拉米苏是我最近学的吗', expectedIndex: 50, type: 'direct', description: '提拉米苏→上周学会' },
  { query: '我去年夏天中暑了吗', expectedIndex: 55, type: 'direct', description: '中暑→去年夏天' },
  { query: 'PMP 什么时候考', expectedIndex: 61, type: 'direct', description: 'PMP→明年' },
  { query: '我通勤要多长时间', expectedIndex: 73, type: 'direct', description: '通勤时间→一个半小时' },

  // ── Additional semantic queries to reach 100 ──
  { query: '我的童年伙伴', expectedIndex: 59, type: 'semantic', description: '童年伙伴→旺财' },
  { query: '我对什么食物反感', expectedIndex: 51, type: 'semantic', description: '食物反感→香菜' },
  { query: '我有什么内容创作经历', expectedIndex: 41, type: 'semantic', description: '内容创作→技术博客' },
  { query: '我的理财经历', expectedIndex: [32, 62], type: 'semantic', description: '理财→炒股亏钱+攒钱目标' },

  // ════════════════════════════════════════════════════════════
  // NEW DIRECT QUERIES (100 more, for memories 80-199)
  // ════════════════════════════════════════════════════════════

  // Memory 80-99: Work details direct
  { query: '我负责什么系统', expectedIndex: 80, type: 'direct', description: '系统→风控' },
  { query: '我们组用什么技术栈', expectedIndex: 81, type: 'direct', description: '技术栈→Go+gRPC+Kafka' },
  { query: '我的 leader 叫什么', expectedIndex: 82, type: 'direct', description: 'leader→王磊' },
  { query: '我上个季度绩效怎么样', expectedIndex: 83, type: 'direct', description: '绩效→B+' },
  { query: '李晨是谁', expectedIndex: 84, type: 'direct', description: '李晨→同事好友' },
  { query: '公司给我配了什么设备', expectedIndex: 85, type: 'direct', description: '设备→两块4K显示器' },
  { query: '我之前在哪家公司', expectedIndex: 86, type: 'direct', description: '之前公司→美团' },
  { query: '入职字节涨了多少薪水', expectedIndex: 87, type: 'direct', description: '涨薪→40%' },
  { query: '我们多久开一次 sprint review', expectedIndex: 88, type: 'direct', description: 'sprint→两周一次' },
  { query: '我最近在做什么 POC', expectedIndex: 89, type: 'direct', description: 'POC→反欺诈模型' },
  { query: '我实习在哪家公司', expectedIndex: 90, type: 'direct', description: '实习→百度' },
  { query: '公司楼下有什么店', expectedIndex: 91, type: 'direct', description: '楼下→星巴克' },
  { query: '你在公司戴什么耳机', expectedIndex: 92, type: 'direct', description: '耳机→降噪' },
  { query: '被 CTO 表扬是因为什么', expectedIndex: 93, type: 'direct', description: 'CTO表扬→架构优化' },
  { query: '小陈去了哪家公司', expectedIndex: 94, type: 'direct', description: '小陈→快手' },
  { query: '你在准备什么述职', expectedIndex: 95, type: 'direct', description: '述职→晋升评审' },
  { query: '你有几年 Go 经验', expectedIndex: 96, type: 'direct', description: 'Go经验→3年' },
  { query: '字节有什么福利', expectedIndex: 97, type: 'direct', description: '福利→三餐健身房体检' },
  { query: '你 GitHub 有多少 star', expectedIndex: 98, type: 'direct', description: 'GitHub→1200 star' },
  { query: '年会你抽到了什么', expectedIndex: 99, type: 'direct', description: '年会→iPad Pro' },

  // Memory 100-119: Family direct
  { query: '你爸是做什么的', expectedIndex: 100, type: 'direct', description: '爸爸→数学老师' },
  { query: '你妈在哪工作', expectedIndex: 101, type: 'direct', description: '妈妈→超市收银员' },
  { query: '你有兄弟姐妹吗', expectedIndex: 102, type: 'direct', description: '兄妹→妹妹小敏' },
  { query: '你妹妹结婚了吗', expectedIndex: 103, type: 'direct', description: '妹妹婚事→去年结婚' },
  { query: '你爷爷还在吗', expectedIndex: 104, type: 'direct', description: '爷爷→去年过世' },
  { query: '你奶奶身体怎么样', expectedIndex: 105, type: 'direct', description: '奶奶→还好独居' },
  { query: '你们过年在哪过', expectedIndex: 106, type: 'direct', description: '过年→长沙老家' },
  { query: '你爸有什么病', expectedIndex: 107, type: 'direct', description: '爸爸病→高血压' },
  { query: '小雨的父母在哪', expectedIndex: 108, type: 'direct', description: '小雨父母→杭州' },
  { query: '你的房子在哪', expectedIndex: 109, type: 'direct', description: '房子→昌平回龙观' },
  { query: '你叔叔做什么生意', expectedIndex: 110, type: 'direct', description: '叔叔→湘菜馆' },
  { query: '你表哥在干嘛', expectedIndex: 111, type: 'direct', description: '表哥→部队连长' },
  { query: '你妈催你什么', expectedIndex: 112, type: 'direct', description: '催婚→结婚' },
  { query: '小雨给你妈买了什么', expectedIndex: 113, type: 'direct', description: '小雨送礼→金项链' },
  { query: '你表弟今年干嘛', expectedIndex: 114, type: 'direct', description: '表弟→高考' },
  { query: '你清明节做什么', expectedIndex: 115, type: 'direct', description: '清明→扫墓' },
  { query: '家里养了什么植物', expectedIndex: 116, type: 'direct', description: '植物→绿萝金鱼' },
  { query: '你爸退休后干嘛', expectedIndex: 117, type: 'direct', description: '爸退休→钓鱼' },
  { query: '你妹妹怀孕了吗', expectedIndex: 118, type: 'direct', description: '妹妹怀孕→两个月' },
  { query: '你和小雨什么时候领证', expectedIndex: 119, type: 'direct', description: '领证→明年' },

  // Memory 120-139: Health/Finance/Education direct
  { query: '你有胃病吗', expectedIndex: 120, type: 'direct', description: '胃病→慢性胃炎' },
  { query: '你多久做一次胃镜', expectedIndex: 121, type: 'direct', description: '胃镜→半年' },
  { query: '你吃什么药', expectedIndex: 122, type: 'direct', description: '药→奥美拉唑莫沙必利' },
  { query: '你甲状腺有问题吗', expectedIndex: 123, type: 'direct', description: '甲状腺→结节' },
  { query: '你腰有什么问题', expectedIndex: 124, type: 'direct', description: '腰→椎间盘突出' },
  { query: '你的椅子多少钱', expectedIndex: 125, type: 'direct', description: '椅子→Herman Miller 8000' },
  { query: '你买了什么基金', expectedIndex: 126, type: 'direct', description: '基金→货币基金10万' },
  { query: '你每月定投多少', expectedIndex: 127, type: 'direct', description: '定投→沪深300 3000' },
  { query: '你买了什么保险', expectedIndex: 128, type: 'direct', description: '保险→百万医疗+重疾' },
  { query: '你退税退了多少', expectedIndex: 129, type: 'direct', description: '退税→4800' },
  { query: '你公积金多少', expectedIndex: 130, type: 'direct', description: '公积金→3200' },
  { query: '你在哪个大学', expectedIndex: 131, type: 'direct', description: '大学→武汉大学' },
  { query: '你毕业设计做了什么', expectedIndex: 132, type: 'direct', description: '毕设→人脸识别' },
  { query: '你大学老师谁讲课好', expectedIndex: 133, type: 'direct', description: '老师→周老师数据结构' },
  { query: '你考研考了几次', expectedIndex: 134, type: 'direct', description: '考研→两次差3分' },
  { query: '你为什么没读研', expectedIndex: 135, type: 'direct', description: '没读研→放弃工作了' },
  { query: '你高中在哪读的', expectedIndex: 136, type: 'direct', description: '高中→长沙一中' },
  { query: '你信用卡额度多少', expectedIndex: 137, type: 'direct', description: '信用卡→5万' },
  { query: '你在理财通有多少存款', expectedIndex: 138, type: 'direct', description: '理财通→5万定期' },
  { query: '你到手工资多少', expectedIndex: 139, type: 'direct', description: '到手→2.8万' },

  // Memory 140-159: Social/Hobby/Routine direct
  { query: '高中同学群谁最活跃', expectedIndex: 140, type: 'direct', description: '群活跃→老赵' },
  { query: '刘毅在做什么', expectedIndex: 141, type: 'direct', description: '刘毅→深圳SaaS创业' },
  { query: '你和同学玩什么游戏', expectedIndex: 142, type: 'direct', description: '同学游戏→狼人杀' },
  { query: '你邻居是什么人', expectedIndex: 143, type: 'direct', description: '邻居→退休夫妇' },
  { query: '黑客马拉松拿了什么奖', expectedIndex: 144, type: 'direct', description: '黑客马拉松→二等奖' },
  { query: '你在 LeetCode 刷了多少题', expectedIndex: 145, type: 'direct', description: 'LeetCode→600题' },
  { query: '你买了几把机械键盘', expectedIndex: 146, type: 'direct', description: '机械键盘→三把' },
  { query: '你原神什么角色满命', expectedIndex: 147, type: 'direct', description: '原神→雷电将军' },
  { query: '你周日下午一般干嘛', expectedIndex: 148, type: 'direct', description: '周日→咖啡馆看书' },
  { query: '你闹钟几点响', expectedIndex: 149, type: 'direct', description: '闹钟→6:50' },
  { query: '走到地铁站要多久', expectedIndex: 150, type: 'direct', description: '走路→15分钟' },
  { query: '你午休怎么休息', expectedIndex: 151, type: 'direct', description: '午休→趴桌上半小时' },
  { query: '你下午喝什么', expectedIndex: 152, type: 'direct', description: '下午→三点咖啡' },
  { query: '你晚饭常点什么外卖', expectedIndex: 153, type: 'direct', description: '外卖→黄焖鸡' },
  { query: '你洗完头用吹风机吗', expectedIndex: 154, type: 'direct', description: '吹风机→完全吹干' },
  { query: '你几点开始洗漱', expectedIndex: 155, type: 'direct', description: '洗漱→十点半' },
  { query: '你健身房的年卡用了吗', expectedIndex: 156, type: 'direct', description: '健身房→去了五次' },
  { query: '你手机有多少照片', expectedIndex: 157, type: 'direct', description: '照片→2万多张' },
  { query: '你用什么做知识管理', expectedIndex: 158, type: 'direct', description: '知识管理→Notion' },
  { query: '你周三晚上和小雨干嘛', expectedIndex: 159, type: 'direct', description: '周三→看综艺' },

  // Memory 160-179: Personality/Life events direct
  { query: '你脾气怎么样', expectedIndex: 160, type: 'direct', description: '脾气→急躁直接' },
  { query: '遇到不公平的事你怎么办', expectedIndex: 161, type: 'direct', description: '不公平→当面说' },
  { query: '你买东西前做什么', expectedIndex: 162, type: 'direct', description: '买东西→看测评对比' },
  { query: '你喜欢大型聚会吗', expectedIndex: 163, type: 'direct', description: '聚会→超十人不自在' },
  { query: '你用什么管理待办事项', expectedIndex: 164, type: 'direct', description: '待办→滴答清单' },
  { query: '你压力大的时候怎么办', expectedIndex: 165, type: 'direct', description: '压力→去江边走' },
  { query: '你什么时候搬到北京的', expectedIndex: 166, type: 'direct', description: '搬北京→2022年' },
  { query: '你在上海住哪', expectedIndex: 167, type: 'direct', description: '上海→浦东张江' },
  { query: '你去年国庆去了哪', expectedIndex: 168, type: 'direct', description: '国庆→西安' },
  { query: '你蜜月打算去哪', expectedIndex: 169, type: 'direct', description: '蜜月→马尔代夫' },
  { query: '你大学时候去过云南吗', expectedIndex: 170, type: 'direct', description: '云南→背包半个月' },
  { query: '你出差去过哪些城市', expectedIndex: 171, type: 'direct', description: '出差→深圳广州成都' },
  { query: '你有选择困难症吗', expectedIndex: 172, type: 'direct', description: '选择困难→点外卖纠结' },
  { query: '你手机是静音的吗', expectedIndex: 173, type: 'direct', description: '手机→静音漏接' },
  { query: '你会主动求人帮忙吗', expectedIndex: 174, type: 'direct', description: '求人→不喜欢麻烦别人' },
  { query: '你情绪不好会怎样', expectedIndex: 175, type: 'direct', description: '情绪差→暴饮暴食' },
  { query: '你有潜水证吗', expectedIndex: 176, type: 'direct', description: '潜水→PADI OW' },
  { query: '你生日收到了什么礼物', expectedIndex: 177, type: 'direct', description: '生日→Apple Watch' },
  { query: '你和前女友为什么分手', expectedIndex: 178, type: 'direct', description: '前女友→异地恋' },
  { query: '你第一份工作在哪', expectedIndex: 179, type: 'direct', description: '第一份→美团实习转正' },

  // Memory 180-199: Specific details direct
  { query: '你用什么手机', expectedIndex: 180, type: 'direct', description: '手机→iPhone 15 Pro Max' },
  { query: '你最讨厌被问什么', expectedIndex: 181, type: 'direct', description: '讨厌问→什么时候结婚' },
  { query: '你用什么 App 听歌', expectedIndex: 182, type: 'direct', description: '听歌→Spotify' },
  { query: '你咖啡怎么喝', expectedIndex: 183, type: 'direct', description: '咖啡→美式不加糖奶' },
  { query: '你通勤时听什么', expectedIndex: 184, type: 'direct', description: '通勤听→播客' },
  { query: '你最近听什么播客', expectedIndex: 185, type: 'direct', description: '播客→硬地骇客' },
  { query: '你什么时候买书', expectedIndex: 186, type: 'direct', description: '买书→618双十一' },
  { query: '你想买什么相机', expectedIndex: 187, type: 'direct', description: '相机→富士X-T5' },
  { query: '你搬家时扔了什么', expectedIndex: 188, type: 'direct', description: '搬家→旧书衣服' },
  { query: '你有什么运动鞋', expectedIndex: 189, type: 'direct', description: '运动鞋→Nike+Adidas' },
  { query: '你睡觉开空调吗', expectedIndex: 190, type: 'direct', description: '空调→必须开' },
  { query: '你用什么浏览器', expectedIndex: 191, type: 'direct', description: '浏览器→Chrome' },
  { query: '你有强迫症吗', expectedIndex: 192, type: 'direct', description: '强迫→反复确认锁门' },
  { query: '你做菜放蒜多吗', expectedIndex: 193, type: 'direct', description: '蒜→放很多' },
  { query: '你多久和爸妈通一次电话', expectedIndex: 194, type: 'direct', description: '通话→每周两次' },
  { query: '读书会你推荐了什么书', expectedIndex: 195, type: 'direct', description: '推荐→黑客与画家' },
  { query: '你冬天穿什么', expectedIndex: 196, type: 'direct', description: '冬天穿→羽绒服' },
  { query: '你经常口腔溃疡吗', expectedIndex: 197, type: 'direct', description: '口腔溃疡→缺维B' },
  { query: '你在搞什么智能家居', expectedIndex: 198, type: 'direct', description: '智能家居→Home Assistant' },
  { query: '你和小雨周末去哪逛', expectedIndex: 199, type: 'direct', description: '逛街→宜家' },

  // ════════════════════════════════════════════════════════════
  // NEW SEMANTIC QUERIES (100 more, for memories 80-199)
  // ════════════════════════════════════════════════════════════

  // Work semantic
  { query: '你每天处理多少流量', expectedIndex: 80, type: 'semantic', description: '流量→2亿请求' },
  { query: '你在公司用什么消息队列', expectedIndex: 81, type: 'semantic', description: '消息队列→Kafka' },
  { query: '你和上级关系怎么样', expectedIndex: 82, type: 'semantic', description: '上级关系→leader nice' },
  { query: '你上次绩效考核通过了吗', expectedIndex: 83, type: 'semantic', description: '绩效考核→B+' },
  { query: '你在公司有没有好朋友', expectedIndex: 84, type: 'semantic', description: '公司朋友→李晨' },
  { query: '你做外卖相关的工作吗', expectedIndex: 86, type: 'semantic', description: '外卖→美团配送算法' },
  { query: '你跳槽涨了多少', expectedIndex: 87, type: 'semantic', description: '跳槽→涨40%' },
  { query: '你在搞机器学习吗', expectedIndex: 89, type: 'semantic', description: '机器学习→XGBoost POC' },
  { query: '你有做搜索引擎的经验吗', expectedIndex: 90, type: 'semantic', description: '搜索→百度搜索推荐' },
  { query: '你在开源社区活跃吗', expectedIndex: 98, type: 'semantic', description: '开源→GitHub 1200 star' },

  // Family semantic
  { query: '你爸是什么职业', expectedIndex: 100, type: 'semantic', description: '爸职业→数学老师' },
  { query: '你妈快退休了吗', expectedIndex: 101, type: 'semantic', description: '退休→妈妈收银员' },
  { query: '你家里有几个孩子', expectedIndex: 102, type: 'semantic', description: '几个孩子→有妹妹' },
  { query: '你家最近有喜事吗', expectedIndex: [103, 118], type: 'semantic', description: '喜事→妹妹结婚/怀孕' },
  { query: '家里有老人去世吗', expectedIndex: 104, type: 'semantic', description: '去世→爷爷' },
  { query: '你过年怎么安排', expectedIndex: 106, type: 'semantic', description: '过年→回长沙' },
  { query: '你爸妈有慢性病吗', expectedIndex: 107, type: 'semantic', description: '慢性病→爸高血压' },
  { query: '你的婚房在哪', expectedIndex: 109, type: 'semantic', description: '婚房→回龙观' },
  { query: '你亲戚做餐饮的吗', expectedIndex: 110, type: 'semantic', description: '餐饮→叔叔湘菜馆' },
  { query: '你和未来丈母娘关系怎样', expectedIndex: 108, type: 'semantic', description: '丈母娘→杭州' },

  // Health/Finance semantic
  { query: '你有什么消化系统的问题', expectedIndex: 120, type: 'semantic', description: '消化→慢性胃炎' },
  { query: '你定期做什么体检', expectedIndex: [121, 123], type: 'semantic', description: '定期体检→胃镜/甲状腺' },
  { query: '你每天要吃药吗', expectedIndex: 122, type: 'semantic', description: '每天吃药→奥美拉唑' },
  { query: '你久坐有什么毛病', expectedIndex: 124, type: 'semantic', description: '久坐→腰椎间盘突出' },
  { query: '你花大钱买过什么办公设备', expectedIndex: 125, type: 'semantic', description: '办公设备→Herman Miller' },
  { query: '你的存款放在哪', expectedIndex: [126, 138], type: 'semantic', description: '存款→蚂蚁财富/理财通' },
  { query: '你有定期投资习惯吗', expectedIndex: 127, type: 'semantic', description: '定期投资→定投' },
  { query: '你的风险保障', expectedIndex: 128, type: 'semantic', description: '风险保障→百万医疗+重疾' },
  { query: '你税务方面有什么经历', expectedIndex: 129, type: 'semantic', description: '税务→退税4800' },
  { query: '你的住房公积金', expectedIndex: 130, type: 'semantic', description: '住房公积金→3200' },

  // Education semantic
  { query: '你拿过什么学业荣誉', expectedIndex: 131, type: 'semantic', description: '学业荣誉→国奖' },
  { query: '你本科的毕业项目', expectedIndex: 132, type: 'semantic', description: '毕业项目→人脸识别' },
  { query: '你印象最深的老师', expectedIndex: [133, 136], type: 'semantic', description: '印象深老师→周老师/刘老师' },
  { query: '你考研失败了吗', expectedIndex: 134, type: 'semantic', description: '考研失败→差3分' },
  { query: '你读了几年学', expectedIndex: [131, 136], type: 'semantic', description: '读书→武大+长沙一中' },

  // Social/Hobby semantic
  { query: '你的创业朋友', expectedIndex: 141, type: 'semantic', description: '创业朋友→刘毅SaaS' },
  { query: '你和同学怎么保持联系', expectedIndex: [140, 142], type: 'semantic', description: '保持联系→群聊+狼人杀' },
  { query: '你和邻居关系好吗', expectedIndex: 143, type: 'semantic', description: '邻居→退休夫妇送菜' },
  { query: '你有什么编程比赛经历', expectedIndex: 144, type: 'semantic', description: '编程比赛→黑客马拉松' },
  { query: '你的算法能力怎么样', expectedIndex: 145, type: 'semantic', description: '算法→LeetCode 600题' },
  { query: '你有什么外设爱好', expectedIndex: 146, type: 'semantic', description: '外设→机械键盘' },
  { query: '你玩什么手游', expectedIndex: 147, type: 'semantic', description: '手游→原神' },
  { query: '你周末有什么固定安排', expectedIndex: [148, 30], type: 'semantic', description: '周末固定→看书/陪孩子' },
  { query: '你赖床吗', expectedIndex: 149, type: 'semantic', description: '赖床→十分钟' },
  { query: '你中午怎么恢复精力', expectedIndex: 151, type: 'semantic', description: '恢复精力→午休趴桌上' },

  // Personality/Life semantic
  { query: '你说话会得罪人吗', expectedIndex: 160, type: 'semantic', description: '得罪人→直来直去' },
  { query: '你是理性消费者吗', expectedIndex: 162, type: 'semantic', description: '理性消费→做功课看测评' },
  { query: '你是内向还是外向', expectedIndex: 163, type: 'semantic', description: '内向外向→不喜欢大场合' },
  { query: '你有什么减压方式', expectedIndex: 165, type: 'semantic', description: '减压→江边散步' },
  { query: '你为什么来北京', expectedIndex: 166, type: 'semantic', description: '来北京→字节offer' },
  { query: '你去西安看了什么', expectedIndex: 168, type: 'semantic', description: '西安→兵马俑大唐不夜城' },
  { query: '你独自旅行过吗', expectedIndex: 170, type: 'semantic', description: '独自旅行→云南半个月' },
  { query: '你有什么坏习惯', expectedIndex: [172, 173, 175], type: 'semantic', description: '坏习惯→选择困难/静音/暴食' },
  { query: '你的恋爱经历', expectedIndex: [1, 178, 119], type: 'semantic', description: '恋爱→小雨/前女友/领证' },
  { query: '你的职业路径', expectedIndex: [179, 86, 0], type: 'semantic', description: '职业路径→美团→字节' },

  // Specific details semantic
  { query: '你是苹果生态的用户吗', expectedIndex: [180, 35, 184], type: 'semantic', description: '苹果→iPhone/MacBook/AirPods' },
  { query: '你听什么类型的音频内容', expectedIndex: [184, 185], type: 'semantic', description: '音频→播客' },
  { query: '你的睡眠习惯', expectedIndex: [190, 155, 10], type: 'semantic', description: '睡眠习惯→空调/洗漱/失眠' },
  { query: '你做饭有什么特点', expectedIndex: [193, 48], type: 'semantic', description: '做饭特点→放蒜多/糖醋排骨' },
  { query: '你和家人怎么沟通', expectedIndex: [194, 112], type: 'semantic', description: '家人沟通→视频通话/催婚' },
  { query: '你对摄影感兴趣吗', expectedIndex: [187, 157], type: 'semantic', description: '摄影→富士相机/2万张照片' },
  { query: '你有什么口腔问题', expectedIndex: 197, type: 'semantic', description: '口腔→溃疡缺维B' },
  { query: '你在折腾什么技术项目', expectedIndex: 198, type: 'semantic', description: '技术项目→Home Assistant' },
  { query: '你周末怎么过', expectedIndex: [199, 148, 30], type: 'semantic', description: '周末→宜家/看书/公园' },
  { query: '你穿衣有什么习惯', expectedIndex: [196, 70], type: 'semantic', description: '穿衣→羽绒服/优衣库Zara' },

  // ════════════════════════════════════════════════════════════
  // HARD QUERIES (100 total — 否定/聚合/跨领域/时间推理/抽象)
  // ════════════════════════════════════════════════════════════

  // Negation queries (否定推理)
  { query: '你有什么做不到的事', expectedIndex: [75, 47, 172], type: 'hard', description: '做不到→开车/小提琴/选择' },
  { query: '你的弱点是什么', expectedIndex: [160, 172, 175], type: 'hard', description: '弱点→急躁/选择困难/暴食' },
  { query: '你不看什么内容', expectedIndex: 78, type: 'hard', description: '不看→娱乐八卦' },
  { query: '你有什么不能吃的', expectedIndex: [51, 120], type: 'hard', description: '不能吃→香菜/不能喝酒吃辣' },
  { query: '你有什么不敢做的事', expectedIndex: [75, 26, 58], type: 'hard', description: '不敢→开车/蛇/打针' },
  { query: '你放弃过什么', expectedIndex: [47, 135, 156], type: 'hard', description: '放弃→小提琴/考研/健身房' },
  { query: '你后悔过什么决定吗', expectedIndex: [135, 32], type: 'hard', description: '后悔→考研/炒股' },
  { query: '你有什么社交障碍', expectedIndex: [163, 160], type: 'hard', description: '社交障碍→不喜欢大聚会/得罪人' },
  { query: '你讨厌什么', expectedIndex: [51, 78, 181], type: 'hard', description: '讨厌→香菜/八卦/被问结婚' },
  { query: '你失败过吗', expectedIndex: [9, 134, 32], type: 'hard', description: '失败→面试被刷/考研/炒股' },

  // Aggregation queries (聚合推理)
  { query: '你每个月的收支是什么样的', expectedIndex: [139, 11, 68, 127, 128], type: 'hard', description: '收支→工资/房贷/网购/定投/保险' },
  { query: '你身上有多少慢性病', expectedIndex: [120, 124, 123, 2, 197], type: 'hard', description: '慢性病→胃炎/腰椎/甲状腺/血压/溃疡' },
  { query: '你的所有社交媒体账号', expectedIndex: [40, 41, 42, 43], type: 'hard', description: '社交媒体→抖音/博客/微信/小红书' },
  { query: '你都在哪些城市生活过', expectedIndex: [17, 4, 167, 166, 109], type: 'hard', description: '城市→长沙/武汉/上海/北京' },
  { query: '列举你的所有数码设备', expectedIndex: [35, 180, 184, 177], type: 'hard', description: '数码→MacBook/iPhone/AirPods/Watch' },
  { query: '你家有哪些人', expectedIndex: [100, 101, 102, 1, 12], type: 'hard', description: '家人→爸/妈/妹妹/女朋友/孩子' },
  { query: '你有哪些运动习惯', expectedIndex: [6, 20, 14, 36, 176], type: 'hard', description: '运动→跑步/篮球/羽毛球/潜水' },
  { query: '你在多少个公司工作过', expectedIndex: [90, 86, 0, 39], type: 'hard', description: '公司→百度/美团/字节' },
  { query: '你学过多少门语言', expectedIndex: [96, 7, 33], type: 'hard', description: '语言→Go/Python/Rust/日语' },
  { query: '你的全部保险和理财', expectedIndex: [126, 127, 128, 138], type: 'hard', description: '保险理财→货基/定投/医疗/定期' },

  // Cross-domain queries (跨领域推理)
  { query: '工作压力对你健康有影响吗', expectedIndex: [19, 124, 10, 55], type: 'hard', description: '工作→健康→加班/腰椎/失眠/中暑' },
  { query: '你的经济状况和生活质量', expectedIndex: [139, 11, 109, 68], type: 'hard', description: '经济生活→工资/房贷/房子/消费' },
  { query: '你的家庭责任', expectedIndex: [63, 12, 112, 194], type: 'hard', description: '家庭责任→盖房/怀孕/催婚/通话' },
  { query: '技术能力如何影响你的职业', expectedIndex: [96, 98, 145, 93], type: 'hard', description: '技术→职业→经验/GitHub/LeetCode/CTO表扬' },
  { query: '你的消费观和收入匹配吗', expectedIndex: [139, 68, 71, 125], type: 'hard', description: '消费收入→工资/网购/盲盒/椅子' },
  { query: '你的通勤影响了生活质量吗', expectedIndex: [72, 73, 150, 19], type: 'hard', description: '通勤影响→地铁/时间/步行/加班' },
  { query: '你的饮食习惯和健康有关系吗', expectedIndex: [120, 17, 51, 183], type: 'hard', description: '饮食健康→胃炎/吃辣/香菜/咖啡' },
  { query: '你的社交圈都是什么类型的人', expectedIndex: [84, 28, 141, 143], type: 'hard', description: '社交圈→同事/室友/创业/邻居' },
  { query: '你的文化生活', expectedIndex: [37, 44, 79, 195], type: 'hard', description: '文化→三体/周杰伦/B站/黑客与画家' },
  { query: '你的线上和线下社交', expectedIndex: [42, 142, 14, 36], type: 'hard', description: '线上线下→微信/狼人杀/篮球/羽毛球' },

  // Temporal reasoning (时间推理)
  { query: '你最近换了什么', expectedIndex: [166, 180, 94], type: 'hard', description: '最近换→搬北京/换手机/同事离职' },
  { query: '你去年发生了什么大事', expectedIndex: [104, 38, 103, 168], type: 'hard', description: '去年→爷爷过世/近视手术/妹妹结婚/西安' },
  { query: '你这个月要做什么', expectedIndex: [95, 18, 89], type: 'hard', description: '这个月→述职/婚礼/POC' },
  { query: '你明年有什么计划', expectedIndex: [61, 119, 169], type: 'hard', description: '明年→PMP/领证/蜜月' },
  { query: '你小时候和现在有什么变化', expectedIndex: [56, 57, 166, 0], type: 'hard', description: '变化→农村→北京→字节' },
  { query: '你最近三个月做了什么', expectedIndex: [89, 93, 94, 146], type: 'hard', description: '三个月→POC/CTO/同事离职/键盘' },
  { query: '你的职业时间线', expectedIndex: [90, 179, 86, 166, 0], type: 'hard', description: '时间线→百度→美团→字节' },
  { query: '你什么时候开始坚持的习惯', expectedIndex: [6, 25, 127], type: 'hard', description: '坚持→跑步三个月/戒烟47天/定投' },
  { query: '你过去一年的旅行', expectedIndex: [168, 5, 27], type: 'hard', description: '旅行→西安/成都/日本计划' },
  { query: '你最近的情感变化', expectedIndex: [12, 119, 118], type: 'hard', description: '情感→怀孕/领证/妹妹怀孕' },

  // Abstract / philosophical queries (抽象推理)
  { query: '你的人生优先级', expectedIndex: [12, 63, 60, 62], type: 'hard', description: '优先级→家庭/父母/梦想/财务' },
  { query: '什么定义了你', expectedIndex: [0, 17, 56, 160], type: 'hard', description: '定义→工作/家乡/童年/性格' },
  { query: '你最骄傲的事', expectedIndex: [93, 57, 98, 131], type: 'hard', description: '骄傲→CTO表扬/竞赛/GitHub/国奖' },
  { query: '你最大的遗憾', expectedIndex: [134, 47, 59], type: 'hard', description: '遗憾→考研/小提琴/旺财' },
  { query: '你的安全感来自哪里', expectedIndex: [1, 128, 109, 139], type: 'hard', description: '安全感→小雨/保险/房子/工资' },
  { query: '你对自己满意吗', expectedIndex: [83, 93, 32, 156], type: 'hard', description: '满意→绩效B+/被表扬/亏钱/健身放弃' },
  { query: '你在逃避什么', expectedIndex: [112, 163, 75], type: 'hard', description: '逃避→催婚/社交/开车' },
  { query: '你的精神世界', expectedIndex: [37, 44, 79, 60], type: 'hard', description: '精神→三体/周杰伦/B站/咖啡店梦' },
  { query: '你的焦虑来源', expectedIndex: [19, 11, 31, 95], type: 'hard', description: '焦虑→加班/房贷/换工作/晋升' },
  { query: '你的幸福时刻', expectedIndex: [12, 8, 5, 177], type: 'hard', description: '幸福→怀孕/妈妈红烧肉/成都/生日礼物' },

  // Paraphrase / synonym queries (同义改写)
  { query: '你的代步工具', expectedIndex: [22, 72, 74], type: 'hard', description: '代步→特斯拉/地铁/单车' },
  { query: '你吃什么保健品', expectedIndex: 122, type: 'hard', description: '保健品→药（模糊边界）' },
  { query: '你有什么证书', expectedIndex: [75, 176, 61], type: 'hard', description: '证书→驾照/PADI OW/PMP计划' },
  { query: '你写过多少代码', expectedIndex: [41, 98, 145], type: 'hard', description: '代码→博客/GitHub/LeetCode' },
  { query: '你的居住环境', expectedIndex: [109, 143, 116], type: 'hard', description: '居住→回龙观/邻居/金鱼绿萝' },
  { query: '你的娱乐开支', expectedIndex: [71, 147, 146], type: 'hard', description: '娱乐开支→盲盒/原神/键盘' },
  { query: '你的屏幕时间', expectedIndex: [40, 66, 67], type: 'hard', description: '屏幕时间→抖音/B站/微博' },
  { query: '你的上下班路线', expectedIndex: [72, 150, 74], type: 'hard', description: '路线→地铁/走路15分/单车' },
  { query: '你的学历背景', expectedIndex: [4, 131, 136], type: 'hard', description: '学历→武汉/武大/长沙一中' },
  { query: '你的副业', expectedIndex: [41, 98], type: 'hard', description: '副业→技术博客/开源项目' },

  // Complex scenario queries (复杂场景)
  { query: '如果你生病了谁照顾你', expectedIndex: [1, 101, 102], type: 'hard', description: '照顾→小雨/妈妈/妹妹' },
  { query: '你退休后会做什么', expectedIndex: [60, 117, 187], type: 'hard', description: '退休→咖啡店/像爸钓鱼/摄影' },
  { query: '你的孩子出生后生活会怎么变', expectedIndex: [12, 109, 139, 19], type: 'hard', description: '孩子出生→预产期/房子/工资/加班' },
  { query: '搬到北京后你失去了什么', expectedIndex: [167, 106, 100], type: 'hard', description: '失去→上海生活/离家远/离父母远' },
  { query: '你觉得自己健康吗', expectedIndex: [120, 124, 10, 2, 197], type: 'hard', description: '健康→胃炎/腰椎/失眠/血压/溃疡' },
  { query: '你最花钱的是什么', expectedIndex: [11, 125, 109], type: 'hard', description: '花钱→房贷/椅子/房子' },
  { query: '你的社会关系网', expectedIndex: [84, 28, 82, 141, 143], type: 'hard', description: '关系网→李晨/张磊/leader/刘毅/邻居' },
  { query: '你的信息获取渠道', expectedIndex: [76, 79, 185, 43], type: 'hard', description: '信息→36kr/B站/播客/小红书' },
  { query: '你人生的转折点', expectedIndex: [166, 134, 178, 0], type: 'hard', description: '转折→搬北京/考研失败/分手/字节offer' },
  { query: '你从父母身上继承了什么', expectedIndex: [100, 17, 107, 2], type: 'hard', description: '继承→数学/湖南/高血压遗传' },

  // ════════════════════════════════════════════════════════════
  // ADDITIONAL SEMANTIC QUERIES (filling to 200 semantic)
  // ════════════════════════════════════════════════════════════

  { query: '你下午犯困怎么办', expectedIndex: 152, type: 'semantic', description: '犯困→咖啡续命' },
  { query: '你最常吃的外卖是什么', expectedIndex: 153, type: 'semantic', description: '常吃→黄焖鸡' },
  { query: '你有洁癖吗', expectedIndex: [154, 192], type: 'semantic', description: '洁癖→吹干头发/确认锁门' },
  { query: '你几点上床', expectedIndex: 155, type: 'semantic', description: '上床→十点半洗漱' },
  { query: '你办了什么会员卡', expectedIndex: 156, type: 'semantic', description: '会员卡→健身房年卡' },
  { query: '你用什么记录生活', expectedIndex: [157, 158], type: 'semantic', description: '记录→拍照/Notion' },
  { query: '你和女朋友的约会活动', expectedIndex: [159, 199], type: 'semantic', description: '约会→看综艺/逛宜家' },
  { query: '你性格上容易吃亏吗', expectedIndex: [160, 174], type: 'semantic', description: '吃亏→直来直去/不求人' },
  { query: '你是完美主义者吗', expectedIndex: [162, 164, 192], type: 'semantic', description: '完美主义→测评/清单/强迫症' },
  { query: '你的散步习惯', expectedIndex: [165, 150], type: 'semantic', description: '散步→江边/走路去地铁' },
  { query: '你住过几个城市', expectedIndex: [17, 4, 167, 109], type: 'semantic', description: '住过→长沙/武汉/上海/北京' },
  { query: '你国庆一般怎么安排', expectedIndex: [168, 5], type: 'semantic', description: '国庆→西安/成都' },
  { query: '你有什么极限运动经历', expectedIndex: 176, type: 'semantic', description: '极限运动→潜水' },
  { query: '你收到过什么印象深刻的礼物', expectedIndex: [177, 99], type: 'semantic', description: '礼物→Apple Watch/iPad Pro' },
  { query: '你之前的感情经历', expectedIndex: 178, type: 'semantic', description: '之前感情→前女友异地' },
  { query: '你从实习到现在多久了', expectedIndex: [90, 179], type: 'semantic', description: '实习至今→百度实习/美团转正' },
  { query: '你以前用安卓吗', expectedIndex: 180, type: 'semantic', description: '安卓→之前一直用' },
  { query: '你为什么不用网易云', expectedIndex: 182, type: 'semantic', description: '不用网易云→版权少' },
  { query: '你喝咖啡加糖吗', expectedIndex: 183, type: 'semantic', description: '加糖→不加糖不加奶' },
  { query: '你通勤路上做什么', expectedIndex: [184, 185], type: 'semantic', description: '通勤路上→听播客' },
  { query: '你有阅读习惯吗', expectedIndex: [186, 148, 37], type: 'semantic', description: '阅读→买书/咖啡馆看书/三体' },
  { query: '你有什么想入手的新装备', expectedIndex: [187, 16], type: 'semantic', description: '新装备→富士相机/特斯拉' },
  { query: '你搬过家吗', expectedIndex: [188, 166], type: 'semantic', description: '搬家→扔东西/上海到北京' },
  { query: '你睡觉有什么讲究', expectedIndex: [190, 10], type: 'semantic', description: '睡觉讲究→空调/失眠' },
  { query: '你出门前有什么仪式', expectedIndex: 192, type: 'semantic', description: '出门仪式→确认锁门' },
  { query: '你做饭口味重吗', expectedIndex: [193, 17], type: 'semantic', description: '口味重→放蒜多/能吃辣' },
  { query: '你和父母感情好吗', expectedIndex: [194, 63, 112], type: 'semantic', description: '父母感情→通话/盖房/催婚' },
  { query: '你有什么阅读推荐', expectedIndex: [195, 37], type: 'semantic', description: '推荐→黑客与画家/三体' },
  { query: '你怕热还是怕冷', expectedIndex: [52, 55], type: 'semantic', description: '怕热冷→怕冷/中暑' },
  { query: '你牙齿有什么问题', expectedIndex: 197, type: 'semantic', description: '牙齿→口腔溃疡' },
  { query: '你家有什么智能设备', expectedIndex: 198, type: 'semantic', description: '智能设备→Home Assistant' },
  { query: '你逛街一般去哪', expectedIndex: [199, 70], type: 'semantic', description: '逛街→宜家/优衣库Zara' },
  { query: '你的咖啡因摄入', expectedIndex: [64, 152, 91, 183], type: 'semantic', description: '咖啡因→早上咖啡/下午咖啡/星巴克/美式' },
  { query: '你的工作环境怎么样', expectedIndex: [92, 85, 91], type: 'semantic', description: '工作环境→降噪/显示器/星巴克' },
  { query: '你有什么竞赛经历', expectedIndex: [57, 144], type: 'semantic', description: '竞赛→数学竞赛/黑客马拉松' },

  // ════════════════════════════════════════════════════════════
  // ADDITIONAL HARD QUERIES (filling to 100 hard)
  // ════════════════════════════════════════════════════════════

  { query: '你同时在学几样东西', expectedIndex: [7, 33, 89, 198], type: 'hard', description: '同时学→Rust/日语/XGBoost/HA' },
  { query: '你的开销比收入大吗', expectedIndex: [139, 11, 68, 71], type: 'hard', description: '开销收入→工资vs房贷/网购/盲盒' },
  { query: '你身边谁最近有变动', expectedIndex: [94, 118, 114], type: 'hard', description: '变动→小陈离职/妹妹怀孕/表弟高考' },
  { query: '描述你的早晨', expectedIndex: [149, 20, 64, 150, 72], type: 'hard', description: '早晨→闹钟/跑步/咖啡/走路/地铁' },
  { query: '你的人际关系有什么冲突', expectedIndex: [160, 82, 112], type: 'hard', description: '冲突→脾气/leader要求高/催婚' },
  { query: '你花在屏幕上的总时间', expectedIndex: [40, 66, 67, 147], type: 'hard', description: '屏幕总时间→抖音/B站/微博/原神' },
  { query: '你的房子相关开支', expectedIndex: [11, 130, 109], type: 'hard', description: '房子开支→房贷/公积金/买房' },
  { query: '你在不同城市的经历', expectedIndex: [17, 4, 167, 166, 171], type: 'hard', description: '城市经历→长沙/武汉/上海/北京/出差' },
  { query: '你的所有恐惧和焦虑', expectedIndex: [26, 58, 52, 19, 95], type: 'hard', description: '恐惧焦虑→蛇/打针/冷/加班/晋升' },
  { query: '影响你人生轨迹的人', expectedIndex: [100, 136, 82, 1], type: 'hard', description: '影响人→爸/班主任刘/leader/小雨' },
  { query: '你的长期投资有哪些', expectedIndex: [127, 126, 138, 128], type: 'hard', description: '长期投资→定投/货基/定期/保险' },
  { query: '你的所有不良习惯', expectedIndex: [40, 175, 172, 156, 10], type: 'hard', description: '不良→抖音/暴食/选择困难/不健身/失眠' },
  { query: '你拥有的所有证书和资质', expectedIndex: [75, 176], type: 'hard', description: '证书资质→驾照/PADI OW' },
  { query: '你最亲近的五个人', expectedIndex: [1, 100, 101, 102, 84], type: 'hard', description: '亲近→小雨/爸/妈/妹妹/李晨' },
  { query: '你这辈子搬了几次家', expectedIndex: [56, 4, 167, 166, 188], type: 'hard', description: '搬家→农村/武汉/上海/北京/扔东西' },
  { query: '你一天喝几杯咖啡', expectedIndex: [64, 152, 91], type: 'hard', description: '咖啡次数→早上/下午/星巴克' },
  { query: '你对字节的整体评价', expectedIndex: [97, 92, 93, 19], type: 'hard', description: '字节评价→福利/噪音/被表扬/加班' },
  { query: '你这几年错过了什么', expectedIndex: [134, 47, 156, 32], type: 'hard', description: '错过→考研/小提琴/健身/炒股' },
  { query: '你现在最担心什么', expectedIndex: [12, 95, 120, 19], type: 'hard', description: '担心→怀孕/晋升/胃炎/加班' },
  { query: '你和小雨的未来规划', expectedIndex: [119, 169, 12, 109], type: 'hard', description: '未来→领证/蜜月/孩子/房子' },
  { query: '你减轻工作疲劳的方式', expectedIndex: [45, 152, 91, 165], type: 'hard', description: '减疲劳→lo-fi/咖啡/星巴克/散步' },
  { query: '你生活中的仪式感', expectedIndex: [64, 192, 155, 194], type: 'hard', description: '仪式→咖啡/锁门/洗漱/视频通话' },
  { query: '你的知识体系', expectedIndex: [96, 145, 41, 158], type: 'hard', description: '知识→技术栈/LeetCode/博客/Notion' },
  { query: '你和家人的距离', expectedIndex: [17, 109, 166, 194], type: 'hard', description: '距离→长沙/北京/搬家/通话' },
  { query: '你生活中的矛盾', expectedIndex: [120, 17, 19, 156], type: 'hard', description: '矛盾→胃炎但吃辣/加班累/不健身' },
  { query: '你的碎片时间都在做什么', expectedIndex: [40, 67, 66, 184], type: 'hard', description: '碎片→抖音/微博/B站/播客' },
  { query: '你有哪些定期要做的事', expectedIndex: [121, 127, 194, 36], type: 'hard', description: '定期→胃镜/定投/通话/羽毛球' },
  { query: '你的食物地图', expectedIndex: [17, 5, 48, 153, 51], type: 'hard', description: '食物→辣/火锅/糖醋排骨/黄焖鸡/香菜' },
  { query: '你的苹果全家桶', expectedIndex: [180, 35, 184, 177], type: 'hard', description: '苹果→iPhone/MacBook/AirPods/Watch' },
  { query: '总结你的性格', expectedIndex: [160, 161, 163, 174, 172], type: 'hard', description: '性格→急躁/正义/内向/独立/纠结' },
]

// ═══════════════════════════════════════════════════════════════
// BENCHMARK
// ═══════════════════════════════════════════════════════════════

function runBenchmark() {
  console.log('═══════════════════════════════════════════════════════════')
  console.log('  cc-soul 无向量召回基准测试')
  console.log('═══════════════════════════════════════════════════════════')
  console.log()

  // 先让 AAM 学习测试记忆（模拟实际使用）
  for (const mem of TEST_MEMORIES) {
    learnAssociation(mem.content, 0.3)
  }

  // Populate fact-store from test memories
  try {
    const factStore = require('./fact-store.ts')
    for (const mem of TEST_MEMORIES) {
      factStore.extractAndStoreFacts?.(mem.content, 'user')
    }
  } catch {}

  let directHits = 0, directTotal = 0
  let semanticHits = 0, semanticTotal = 0
  let hardHits = 0, hardTotal = 0
  let top1Hits = 0
  const failures: { query: string; type: string; desc: string; got: string[] }[] = []

  for (const tc of TEST_CASES) {
    const results = activationRecall(TEST_MEMORIES, tc.query, 3, 0, 0.5) as Memory[]
    const resultContents = results.map(r => r.content)
    const indices = Array.isArray(tc.expectedIndex) ? tc.expectedIndex : [tc.expectedIndex]
    const expectedContents = indices.map(i => TEST_MEMORIES[i].content)
    const hit = expectedContents.some(ec => resultContents.includes(ec))
    const isTop1 = expectedContents.some(ec => resultContents[0] === ec)

    if (tc.type === 'direct') {
      directTotal++
      if (hit) directHits++
    } else if (tc.type === 'semantic') {
      semanticTotal++
      if (hit) semanticHits++
    } else {
      hardTotal++
      if (hit) hardHits++
    }
    if (isTop1) top1Hits++

    if (!hit) {
      failures.push({
        query: tc.query,
        type: tc.type,
        desc: tc.description,
        got: resultContents.map(c => c.slice(0, 30)),
      })
    }

    const mark = hit ? (isTop1 ? '✅' : '🟡') : '❌'
    console.log(`${mark} [${tc.type.padEnd(8)}] ${tc.description.padEnd(20)} | ${tc.query}`)
  }

  const allHits = directHits + semanticHits + hardHits
  const allTotal = directTotal + semanticTotal + hardTotal

  console.log()
  console.log('═══════════════════════════════════════════════════════════')
  console.log('  结果汇总')
  console.log('═══════════════════════════════════════════════════════════')
  console.log()
  const directRate = (directHits / directTotal * 100).toFixed(0)
  const semanticRate = (semanticHits / semanticTotal * 100).toFixed(0)
  const hardRate = (hardHits / hardTotal * 100).toFixed(0)
  const totalRate = (allHits / allTotal * 100).toFixed(0)
  const top1Rate = (top1Hits / allTotal * 100).toFixed(0)

  console.log(`  直接召回 (top-3):  ${directHits}/${directTotal} = ${directRate}%`)
  console.log(`  语义召回 (top-3):  ${semanticHits}/${semanticTotal} = ${semanticRate}%`)
  console.log(`  困难召回 (top-3):  ${hardHits}/${hardTotal} = ${hardRate}%`)
  console.log(`  总体 (top-3):      ${allHits}/${allTotal} = ${totalRate}%`)
  console.log(`  Top-1 准确率:      ${top1Hits}/${allTotal} = ${top1Rate}%`)
  console.log()

  if (failures.length > 0) {
    console.log('  ── 失败用例 ──')
    for (const f of failures) {
      console.log(`  ❌ [${f.type}] ${f.desc}: "${f.query}"`)
      console.log(`     实际返回: ${f.got.join(' | ')}`)
    }
  }
}

runBenchmark()
