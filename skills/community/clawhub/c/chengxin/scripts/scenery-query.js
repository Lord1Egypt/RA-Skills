#!/usr/bin/env node

/**
 * 同程程心大模型 - 景点专用查询 API
 * 
 * 用法：
 *   node scenery-query.js --destination "杭州"
 *   node scenery-query.js --destination "杭州" --extra "适合亲子"
 *   node scenery-query.js --destination "苏州" --extra "园林 5A 景区"
 *   node scenery-query.js --destination "杭州" --extra "免费 夜景"
 *   node scenery-query.js --destination "杭州" --extra "适合亲子 最便宜"
 * 
 * 参数说明：
 *   --destination <城市>      目的地城市
 *   --extra <补充信息>        额外信息（特色、类型、价格偏好、时段偏好等）
 *   --channel <渠道>          通信渠道（webchat/wechat 等）
 *   --surface <界面>          交互界面（mobile/desktop/table/card）
 * 
 * 配置（优先级：环境变量 > config.json）：
 *   - CHENGXIN_API_KEY（环境变量）
 *   - 或创建 config.json 文件（见 config.example.json）
 */

const { create_query_runner } = require('./lib/base-query');
const { NO_MATCH_DETAIL, MORE_CHOICES_PROMPT } = require('./lib/query-response');
const { format_scenery_card, format_scenery_table } = require('./lib/formatters');

// 景区 API 路径
const SCENERY_API_PATH = '/sceneryResource';

/**
 * 验证参数组合
 * @param {object} params - 参数对象
 * @returns {object} - { valid: boolean, error: string }
 */
function validate_params(params) {
  if (params.destination) {
    return { valid: true };
  }
  
  return { 
    valid: false, 
    error: `⚠️ 参数不完整，请提供目的地城市。
  示例：--destination "杭州"`
  };
}

/**
 * 格式化景点结果
 * @param {object} scenery_data - 景点数据
 * @param {boolean} use_table - 是否使用表格格式
 * @param {boolean} use_plain_link - 是否使用纯文本链接（转发给底层格式化函数）
 * @returns {string} - 格式化输出
 */
function format_scenery_result(scenery_data, use_table = false, use_plain_link = false) {
  if (!scenery_data || !scenery_data.sceneryList) {
    return '未找到相关景区信息';
  }
  
  const sceneries = scenery_data.sceneryList;
  const need_extend = scenery_data.needExtend || false;
  // needExtend=true 时强制使用卡片格式
  const force_card = need_extend;
  
  let output = '🏞️ 景区查询结果：\n\n';
  
  if (use_table && !force_card) {
    output += format_scenery_table(sceneries, use_plain_link);
  } else {
    sceneries.forEach((scenery) => {
      output += format_scenery_card(scenery, use_plain_link, need_extend);
    });
  }
  
  output += MORE_CHOICES_PROMPT;
  output += '\n';
  return output;
}

/**
 * 处理查询结果
 */
function handle_result(response_data, { print_success_once, format_options, print_no_match }) {
  const { use_table, use_plain_link } = format_options;
  const scenery_data_list = response_data?.sceneryDataList;

  if (Array.isArray(scenery_data_list) && scenery_data_list.length > 0) {
    let has_output = false;
    scenery_data_list.forEach((item, index) => {
      if (item.sceneryList && item.sceneryList.length > 0) {
        print_success_once();
        if (item.desc) {
          console.log(`📌 ${item.desc}\n`);
        } else if (scenery_data_list.length > 1) {
          console.log(`📌 列表 ${index + 1}\n`);
        }
        console.log(format_scenery_result(item, use_table, use_plain_link));
        has_output = true;
      }
    });
    if (!has_output) {
      print_no_match();
    }
  } else {
    print_no_match();
  }
}

// 创建查询运行器
const runner = create_query_runner({
  api_path: SCENERY_API_PATH,
  param_defs: {
    destination: '',
    extra: '',
    channel: '',
    surface: ''
  },
  validate: validate_params,
  handle_result: handle_result,
  no_match_detail: NO_MATCH_DETAIL.SCENERY,
  usage_example: `  node scenery-query.js --destination "杭州"
  node scenery-query.js --destination "杭州" --extra "适合亲子"
  node scenery-query.js --destination "苏州" --extra "园林 5A 景区"`
});

// 导出函数供其他模块使用
module.exports = {
  validate_params,
  format_scenery_result
};

// 运行主函数
if (require.main === module) {
  runner.run();
}
