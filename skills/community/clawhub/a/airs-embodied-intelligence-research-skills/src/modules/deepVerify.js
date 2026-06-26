import { delay } from '../browser.js';
import { logger } from '../utils/logger.js';
import { withRetry } from '../utils/retry.js';

/**
 * 进入招投标详情页，抓取完整信息
 * 
 * @param {import('puppeteer-core').Page} page
 * @param {string} detailUrl - 招投标详情页 URL
 * @param {string} title - 项目标题（用于日志）
 * @returns {Promise<Object>} 详细信息
 */
export async function fetchBiddingDetail(page, detailUrl, title) {
  return withRetry(async () => {
    logger.info(`  核查: ${title}`);
    
    await page.goto(detailUrl, { waitUntil: 'networkidle2', timeout: 30000 });
    await delay(2000, 4000);

    // 检查验证码
    const needVerify = await page.evaluate(() => {
      return !!document.querySelector('.verify-modal, .captcha, [class*="verify-wrap"]');
    }).catch(() => false);
    if (needVerify) {
      logger.warn(`⚠️ 出现验证码，请手动处理...`);
      await page.waitForFunction(() => {
        return !document.querySelector('.verify-modal, .captcha, [class*="verify-wrap"]');
      }, { timeout: 120000 }).catch(() => {});
    }

    // 抓取详情页内容
    const detail = await page.evaluate(() => {
      const getText = (selectors) => {
        for (const sel of selectors) {
          const el = document.querySelector(sel);
          if (el) return el.textContent.trim();
        }
        return '';
      };

      // 黑名单：这些值不可能是有效的单位名称
      const BLACKLIST = [
        '成交金额', '中标金额', '预算金额', '金额', '价格',
        '二、其他', '一、其他', '三、其他',
        '选择理由', '中标理由', '推荐理由',
        '包号', '序号', '标段', '标包',
        '主要标的名称', '标的名称', '货物名称',
        '单位名称（公章或合同章）', '地址', '代理机构',
        '0-10分', '内容'
      ];

      const VALID_SUFFIXES = ['公司', '大学', '学院', '研究院', '研究所', '局', '厅', '中心', '学校', '医院', '银行', '集团'];

      // 地址关键词：含这些词的通常不是企业/机构名称
      const ADDRESS_KEYWORDS = ['地点：', '地址：', '开标室', '会议室', '开标地点', '评审地点',
        '楼', '层', '路', '街', '号', '幢', '单元', '室）', '室('];

      function isGarbageValue(val) {
        if (!val || val.length < 2) return true;
        for (const b of BLACKLIST) {
          if (val.includes(b)) return true;
        }
        return false;
      }

      function isValidEntity(val) {
        if (isGarbageValue(val)) return false;
        // 排除明显是地址的文本
        for (const kw of ADDRESS_KEYWORDS) {
          if (val.includes(kw)) return false;
        }
        // 排除纯数字或金额格式
        if (/^[\d,.]+$/.test(val.replace(/[¥￥\s]/g, ''))) return false;
        // 至少包含一个有效的机构后缀，或是纯英文/数字组合（长度>=3）
        if (val.length >= 3 && /^[A-Za-z0-9\s]+$/.test(val)) return true;
        for (const s of VALID_SUFFIXES) {
          if (val.includes(s)) return true;
        }
        return false;
      }

      // 尝试从详情页提取关键信息
      const fullText = document.body.innerText || '';
      
      const result = {
        projectName: '',
        bidder: '',       // 招标人
        winner: '',       // 中标人
        amount: '',       // 金额
        publishDate: '',  // 发布日期
        endDate: '',      // 截止日期
        region: '',       // 地区
        category: '',     // 类别
        content: '',      // 详情内容
        productName: '',  // 产品/货物名称
        productModel: '', // 产品/货物型号
        source: '天眼查', // 数据源
        pageUrl: window.location.href,
      };

      // 辅助：从键值对文本中提取值
      const extractValue = (text) => {
        let val = text.replace(/^[\s\S]*?[：:]\s*/, '').trim();
        // 清理后续混杂的其他字段（如"地点：xxx"后面跟着"预算：yyy"）
        val = val.replace(/(预算金额|发布时间|开标地点|评审地点|代理地址)[：:].*$/, '').trim();
        return val;
      };

      // 1) 先从键值对元素中提取（排除 table tr，避免表格整行文本污染）
      const infoItems = document.querySelectorAll(
        '.detail-list li, .info-list .info-item, ' +
        '.detail-content .item, [class*="detail"] .row'
      );
      
      for (const item of infoItems) {
        const text = item.textContent.trim();
        
        if (/^(项目名称|标题)[：:\s]/.test(text) && !result.projectName) {
          result.projectName = extractValue(text);
        }
        if (/^(招标人|采购人|需求方)[：:\s]/.test(text) && !result.bidder) {
          const val = extractValue(text);
          if (isValidEntity(val)) result.bidder = val;
        }
        if (/^(中标人|供应商名称|中标单位|成交供应商|中标（成交）供应商)[：:\s]/.test(text) && !result.winner) {
          const val = extractValue(text);
          if (isValidEntity(val)) result.winner = val;
        }
        if (/^(中标金额|成交金额|中标（成交）金额)[：:\s]/.test(text) && !result.amount) {
          result.amount = extractValue(text);
        }
        if (/^(金额|预算|价格)[：:\s]/.test(text) && !result.amount) {
          result.amount = extractValue(text);
        }
        if (/^(发布日期|发布时间|公告日期)[：:\s]/.test(text) && !result.publishDate) {
          result.publishDate = extractValue(text);
        }
        if (/^(地区|所在地|行政区域)[：:\s]/.test(text) && !result.region) {
          result.region = extractValue(text);
        }
        if (/^(类别|分类|行业)[：:\s]/.test(text) && !result.category) {
          result.category = extractValue(text);
        }
        if (/^(货物名称|产品名称|标的名称)[：:\s]/.test(text) && !result.productName) {
          result.productName = extractValue(text);
        }
        if (/^(货物型号|产品型号|规格型号)[：:\s]/.test(text) && !result.productModel) {
          result.productModel = extractValue(text);
        }
      }

      // 2) 专门解析表格：识别表头，按列提取中标人/采购人
      const tables = document.querySelectorAll('table');
      const winnerHeaders = ['供应商名称', '中标人', '中标单位', '成交供应商', '中标（成交）供应商', '中标候选人'];
      const bidderHeaders = ['采购人', '招标人', '采购单位', '招采单位', '需求方'];
      const amountHeaders = ['中标金额', '成交金额', '中标（成交）金额'];
      const amountFallbackHeaders = ['金额', '价格', '预算'];

      // 收集所有表格数据，优先用精确匹配的表头
      const tableData = [];
      for (const table of tables) {
        const rows = Array.from(table.querySelectorAll('tr'));
        if (rows.length < 2) continue;

        // 找表头行（th 数量最多的行，或第一行）
        let headerRow = rows[0];
        let maxTh = headerRow.querySelectorAll('th, td').length;
        for (const row of rows) {
          const cellCount = row.querySelectorAll('th, td').length;
          if (cellCount > maxTh) {
            maxTh = cellCount;
            headerRow = row;
          }
        }

        const headerCells = Array.from(headerRow.querySelectorAll('th, td')).map(c => c.textContent.trim().replace(/\s+/g, ''));

        // 定位列索引
        let winnerIdx = -1;
        let bidderIdx = -1;
        let amountIdx = -1;
        let amountIsExact = false;

        for (let i = 0; i < headerCells.length; i++) {
          const h = headerCells[i];
          if (winnerIdx === -1 && winnerHeaders.some(wh => h.includes(wh))) winnerIdx = i;
          if (bidderIdx === -1 && bidderHeaders.some(bh => h.includes(bh))) bidderIdx = i;
          if (amountIdx === -1) {
            if (amountHeaders.some(ah => h.includes(ah))) {
              amountIdx = i;
              amountIsExact = true;
            } else if (amountFallbackHeaders.some(ah => h.includes(ah))) {
              amountIdx = i;
            }
          }
        }

        // 遍历数据行取第一个非空值
        for (const row of rows) {
          if (row === headerRow) continue;
          const cells = Array.from(row.querySelectorAll('td, th'));
          if (cells.length < 2) continue;

          if (winnerIdx !== -1 && cells[winnerIdx]) {
            const val = cells[winnerIdx].textContent.trim();
            if (val && val.length > 1 && !/^(供应商|中标人|中标单位)[：:：\s]/.test(val) && isValidEntity(val)) {
              tableData.push({ type: 'winner', val, isExact: true });
            }
          }
          if (bidderIdx !== -1 && cells[bidderIdx]) {
            const val = cells[bidderIdx].textContent.trim();
            if (val && val.length > 1 && !/^(采购人|招标人)[：:：\s]/.test(val) && isValidEntity(val)) {
              tableData.push({ type: 'bidder', val, isExact: true });
            }
          }
          if (amountIdx !== -1 && cells[amountIdx]) {
            const val = cells[amountIdx].textContent.trim();
            if (val && /\d/.test(val)) {
              tableData.push({ type: 'amount', val, isExact: amountIsExact });
            }
          }
        }
      }

      // 从收集的表格数据中择优选取
      for (const item of tableData) {
        if (item.type === 'winner' && !result.winner) result.winner = item.val;
        if (item.type === 'bidder' && !result.bidder) result.bidder = item.val;
        if (item.type === 'amount' && !result.amount) {
          result.amount = item.val;
        } else if (item.type === 'amount' && result.amount && !result.amount.includes('万元') && item.val.includes('万元')) {
          // 如果已有的金额没有单位，优先使用带"万元"的
          result.amount = item.val;
        }
      }

      // 尝试获取详情正文
      const contentEl = document.querySelector(
        '.detail-content, .bid-detail, .content-text, ' +
        '[class*="detail-body"], [class*="content"], article'
      );
      if (contentEl) {
        result.content = contentEl.textContent.trim().substring(0, 2000);
      }
      
      // 获取完整页面内容（用于 LLM 解析）
      // 优先抓取主要内容区域，包含表格和正文
      const mainContentEl = document.querySelector(
        '.detail-content, .bid-detail, .content-wrapper, ' +
        '[class*="detail-main"], [class*="content-body"], ' +
        'main, article, .container'
      );
      if (mainContentEl) {
        // 转换为类 Markdown 格式
        let mdContent = '';
        
        // 提取标题
        const h1 = document.querySelector('h1, .title');
        if (h1) {
          mdContent += '# ' + h1.textContent.trim() + '\n\n';
        }
        
        // 提取所有表格（转换为 Markdown 表格）
        const tables = mainContentEl.querySelectorAll('table');
        tables.forEach((table, idx) => {
          const rows = table.querySelectorAll('tr');
          if (rows.length > 0) {
            mdContent += '## 表格 ' + (idx + 1) + '\n\n';
            rows.forEach(row => {
              const cells = row.querySelectorAll('td, th');
              const rowData = [];
              cells.forEach(cell => {
                rowData.push(cell.textContent.trim().replace(/\|/g, '\\|'));
              });
              if (rowData.length > 0) {
                mdContent += '| ' + rowData.join(' | ') + ' |\n';
              }
            });
            mdContent += '\n';
          }
        });
        
        // 提取段落文本
        const paragraphs = mainContentEl.querySelectorAll('p, div[class*="text"], div[class*="desc"]');
        if (paragraphs.length > 0) {
          mdContent += '## 正文\n\n';
          paragraphs.forEach(p => {
            const text = p.textContent.trim();
            if (text.length > 10 && text.length < 500) {
              mdContent += text + '\n\n';
            }
          });
        }
        
        // 如果以上都没抓到，直接保存文本内容
        if (mdContent.length < 100) {
          mdContent = mainContentEl.textContent.trim();
        }
        
        result.rawContent = mdContent.substring(0, 10000); // 限制长度
      } else {
        // 备选：保存 body 文本
        result.rawContent = document.body.textContent.trim().substring(0, 5000);
      }

      // 如果项目名称为空，从标题获取
      if (!result.projectName) {
        const h1 = document.querySelector('h1, .title, .header-title');
        if (h1) result.projectName = h1.textContent.trim();
      }

      // 如果产品名称为空，从内容中提取关键词
      if (!result.productName && result.content) {
        // 尝试匹配常见机器人产品名称
        const robotKeywords = ['机器人', '机械臂', '机械手', 'AGV', 'AMR', '人形机器人', '四足机器人', '仿生机器人'];
        for (const kw of robotKeywords) {
          if (result.content.includes(kw)) {
            // 提取包含关键词的短语（前后10个字符）
            const match = result.content.match(new RegExp(`.{0,10}${kw}.{0,10}`));
            if (match) {
              result.productName = match[0].trim();
              break;
            }
          }
        }
      }

      return result;
    });

    return detail;
  }, { maxRetries: 2, delayMs: 3000, label: `核查${title}` });
}

/**
 * 初步判断招投标记录是否可能符合入库标准
 * （基于文本关键词的粗筛，非替代人工审核）
 */
export function preliminaryCheck(record) {
  const reasons = [];
  
  // 排除展会/展览
  const excludeKeywords = ['展览', '展会', '展示', '发布会', '春晚', '表演', '演出'];
  for (const kw of excludeKeywords) {
    if (record.title?.includes(kw) || record.content?.includes(kw)) {
      reasons.push(`包含排除关键词: ${kw}`);
    }
  }

  // 排除纯融资
  if (/融资|投资|增资/.test(record.title) && !/采购|部署|交付/.test(record.title)) {
    reasons.push('疑似纯融资事件');
  }

  // 排除零部件
  const partKeywords = ['减速机', '减速器', '关节模组', '丝杠', '编码器', '传感器'];
  const isPartSupply = partKeywords.some(kw => 
    record.title?.includes(kw) && !record.title?.includes('机器人')
  );
  if (isPartSupply) {
    reasons.push('疑似零部件供应链合作');
  }

  return {
    passed: reasons.length === 0,
    reasons,
  };
}
