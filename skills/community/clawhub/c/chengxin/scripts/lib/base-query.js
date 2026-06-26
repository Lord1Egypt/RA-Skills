#!/usr/bin/env node

/**
 * 同程程心查询基类
 *
 * 抽象共享样板代码，提供通用的查询执行流程
 * 
 * 使用方式：
 *   const { create_query_runner } = require('./lib/base-query');
 *   
 *   const runner = create_query_runner({
 *     api_path: '/trainResource',
 *     param_defs: { departure: '', destination: '', departure_station: '', arrival_station: '', train_number: '', extra: '', channel: '', surface: '' },
 *     validate: (params) => { /* 验证逻辑 *\/ },
 *     handle_result: (response_data, options) => { /* 结果处理 *\/ },
 *     no_match_detail: '未找到相关车次信息',
 *     usage_example: 'node train-query.js --departure "北京" --destination "上海"'
 *   });
 *   
 *   runner.run();
 */

const { call_api } = require('./api-client');
const { resolve_output_mode } = require('./output-mode');
const { extract_response_data } = require('./data-utils');
const {
  NO_MATCH_DETAIL,
  create_success_banner_once,
  handle_api_result,
  print_no_match_lines,
  print_request_exception
} = require('./query-response');

/**
 * 清洗字符串参数：移除控制字符，超长截断
 * 
 * @param {string} value - 原始参数值
 * @param {number} [max_len=500] - 最大长度（仅对自由文本参数生效）
 * @returns {string} 清洗后的参数值
 */
function sanitize_string_arg(value, max_len = 500) {
  if (typeof value !== 'string') return value;
  // 移除控制字符（保留 \t \n \r）
  let cleaned = value.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '');
  // 超长截断
  if (cleaned.length > max_len) {
    cleaned = cleaned.substring(0, max_len) + '…';
  }
  return cleaned;
}

/**
 * 通用参数解析器
 * 
 * 支持两种参数格式：
 * 1. 标准格式：--key value（key 中的连字符会自动转换为下划线）
 * 2. Flag 格式：--key（无值，布尔参数设为 true）或 --key true/false/1/0
 * 
 * @param {object} param_defs - 参数定义对象，键为参数名（小写下划线格式），值为默认值
 * @returns {object} 解析后的参数对象
 */
function parse_args(param_defs) {
  const args = process.argv.slice(2);
  const params = { ...param_defs };
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg.startsWith('--')) {
      // 标准格式或 flag 格式：--key [value]
      const raw_key = arg.slice(2);
      // 将连字符转换为下划线（--departure-station → departure_station）
      const key = raw_key.replace(/-/g, '_');
      
      if (key in params) {
        const next_arg = args[i + 1];
        
        // 检查下一个参数是否是值（不是另一个选项）
        if (next_arg && !next_arg.startsWith('--')) {
          // 有值：处理 true/false/1/0 或普通字符串
          const val = args[++i];
          if (typeof params[key] === 'boolean') {
            // 布尔参数：转换字符串值为布尔
            params[key] = val === 'true' || val === '1';
          } else {
            // 普通参数：清洗后赋值（过滤控制字符，超长截断）
            params[key] = sanitize_string_arg(val);
          }
        } else if (typeof params[key] === 'boolean') {
          // 无值：flag 参数，设为 true
          params[key] = true;
        }
      }
    }
  }
  
  return params;
}

/**
 * 将 snake_case 键名转换为 camelCase
 * 
 * @param {string} key - snake_case 格式的键名
 * @returns {string} camelCase 格式的键名
 */
function to_camel_case(key) {
  return key.replace(/_([a-z])/g, (_, c) => c.toUpperCase());
}

/**
 * 构建请求参数（只包含非空字段，键名转为 camelCase）
 * 
 * @param {object} params - 解析后的参数对象（snake_case 键名）
 * @returns {object} 过滤后的请求参数（camelCase 键名，适配 API 要求）
 */
function build_request_params(params) {
  const request_params = {};
  
  for (const [key, value] of Object.entries(params)) {
    if (value !== '' && value !== null && value !== undefined) {
      const camel_key = to_camel_case(key);
      // extra 字段可能承载大量用户需求，单独放宽长度限制
      const final_value = (camel_key === 'extra' && typeof value === 'string')
        ? sanitize_string_arg(value, 1000)
        : value;
      request_params[camel_key] = final_value;
    }
  }
  
  return request_params;
}

/**
 * 创建查询运行器
 * 
 * @param {object} config - 查询配置
 * @param {string} config.api_path - API 路径（如 /trainResource）
 * @param {object} config.param_defs - 参数定义对象（如 { departure: '', destination: '', departure_station: '' }，键名使用小写下划线格式）
 * @param {function} config.validate - 验证函数，返回 { valid: boolean, error?: string }
 * @param {function} config.handle_result - 结果处理函数，接收 (response_data, options) 参数
 * @param {string} config.no_match_detail - 无匹配结果提示
 * @param {string} config.usage_example - 用法示例（多行字符串，命令行参数使用连字符格式如 --departure-station）
 * @param {object} [config.param_descriptions] - 参数描述对象（可选，用于自定义 --help 输出，键名使用小写下划线格式）
 * @returns {object} 查询运行器对象
 */
function create_query_runner(config) {
  const {
    api_path,
    param_defs,
    validate,
    handle_result,
    no_match_detail,
    usage_example,
    param_descriptions = {}
  } = config;
  
  /**
   * 打印用法信息
   */
  function print_usage() {
    console.log('用法：');
    console.log(usage_example);
    console.log('\n参数说明：');
    
    // 默认描述（当未配置 param_descriptions 时使用）
    const defaultDescriptions = {
      departure: '出发地城市',
      destination: '目的地城市',
      departure_station: '出发站（精确）',
      arrival_station: '到达站（精确）',
      train_number: '车次号',
      flight_number: '航班号',
      low_price: '查询特价/低价',
      extra: '额外信息（日期、偏好等）',
      channel: '通信渠道（webchat/wechat 等）',
      surface: '交互界面（mobile/desktop/table/card）'
    };
    
    for (const [key, defaultValue] of Object.entries(param_defs)) {
      // 优先级：自定义描述 > 默认描述 > 参数名
      const desc = param_descriptions[key] || defaultDescriptions[key] || key;
      const required = !defaultValue ? '（必填）' : '（可选）';
      // 将下划线转回连字符显示（departure_station → --departure-station）
      const cli_key = key.replace(/_/g, '-');
      console.log(`  --${cli_key} <值>          ${desc} ${required}`);
    }
  }
  
  /**
   * 执行查询
   */
  async function run() {
    // 0. 检查 --help / -h 参数
    if (process.argv.includes('--help') || process.argv.includes('-h')) {
      print_usage();
      process.exit(0);
    }

    // 1. 解析参数
    const params = parse_args(param_defs);
    
    // 2. 验证参数
    const validation = validate(params);
    if (!validation.valid) {
      print_usage();
      console.log('\n' + validation.error);
      process.exit(1);
    }
    
    // 3. 构建请求参数
    const request_params = build_request_params(params);
    
    // 4. 检测输出格式
    const { use_table, use_plain_link } = resolve_output_mode(params);
    const format_options = { use_table, use_plain_link };
    
    // 5. 调用 API
    try {
      const result = await call_api(api_path, request_params);
      
      // 6. 处理结果
      handle_api_result(result, {
        no_match_detail: no_match_detail,
        on_success: (res) => {
          const print_success_once = create_success_banner_once();
          // 解包业务数据：防御性双层解包
          // 部分 API 响应为双层嵌套 { code, data: { code, data: {...} } }，
          // 也有单层 { code, data: {...} } 的情况；此处兼容两种格式
          let response_data = extract_response_data(res);
          if (response_data && response_data.data !== undefined &&
              (response_data.code === '0' || response_data.code === 0)) {
            response_data = response_data.data;
          }
          
          // 调用自定义结果处理函数
          handle_result(response_data, {
            print_success_once,
            format_options,
            print_no_match: () => print_no_match_lines(no_match_detail),
            request_params
          });
        }
      });
    } catch (error) {
      print_request_exception(error);
    }
  }
  
  return {
    parse_args: () => parse_args(param_defs),
    run
  };
}

module.exports = {
  create_query_runner,
  parse_args,
  build_request_params
};
