#!/usr/bin/env node

/**
 * 同程程心大模型 - 旅行资源专用查询 API
 * 
 * 用法：
 *   node travel-query.js --destination "三亚"
 *   node travel-query.js --destination "三亚" --extra "五一假期"
 *   node travel-query.js --destination "云南" --extra "6天5晚 自由行"
 * 
 * 参数说明：
 *   --destination <城市/地区>  目的地城市或地区
 *   --extra <补充信息>        额外信息（假期、天数、类型等）
 *   --channel <渠道>          通信渠道（webchat/wechat 等）
 *   --surface <界面>          交互界面（mobile/desktop/table/card）
 * 
 * 说明：
 *   本接口用于查询自由行、跟团游等度假产品
 *   作为用户有明确旅游意向时的补充推荐
 *   如果有合适的单品资源（机票、酒店），应提供更多选择
 * 
 * 配置（优先级：环境变量 > config.json）：
 *   - CHENGXIN_API_KEY（环境变量）
 *   - 或创建 config.json 文件（见 config.example.json）
 */

const { create_query_runner } = require('./lib/base-query');
const { NO_MATCH_DETAIL, MORE_CHOICES_PROMPT } = require('./lib/query-response');
const {
  format_trip_card,
  format_trip_table,
  format_trip_plans,
  format_train_table,
  format_hotel_table,
  format_scenery_table,
  format_scenery_card
} = require('./lib/formatters');

// 度假产品 API 路径
const TRAVEL_API_PATH = '/travelResource';

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
    error: `⚠️ 参数不完整，请提供目的地城市或地区。
  示例：--destination "三亚"`
  };
}

/**
 * 格式化旅行产品结果
 * @param {object} trip_data - 旅行产品数据
 * @param {boolean} use_table - 是否使用表格格式
 * @param {boolean} use_plain_link - 是否使用纯文本链接（转发给底层格式化函数）
 */
function format_travel_result(trip_data, use_table = false, use_plain_link = false) {
  if (!trip_data || !trip_data.tripList) {
    return '';
  }
  
  const trips = trip_data.tripList;
  let output = '🧳 **度假产品**\n\n';
  
  if (use_table) {
    output += format_trip_table(trips, use_plain_link);
  } else {
    trips.forEach((trip) => {
      output += format_trip_card(trip, use_plain_link);
    });
  }
  
  return output;
}

/**
 * 格式化火车票结果
 * @param {Array} train_data_list - 火车数据列表
 * @param {boolean} use_table - 是否使用表格格式
 * @param {boolean} use_plain_link - 是否使用纯文本链接（转发给底层格式化函数）
 */
function format_train_result(train_data_list, use_table = false, use_plain_link = false) {
  if (!train_data_list || train_data_list.length === 0) {
    return '';
  }

  let output = '🚄 **推荐火车/高铁**\n\n';

  train_data_list.forEach((item) => {
    if (item.desc) {
      output += `📌 ${item.desc}\n`;
    }
    if (item.trainList && item.trainList.length > 0) {
      output += format_train_table(item.trainList, use_plain_link);
      output += '\n';
    }
  });

  return output;
}

/**
 * 格式化酒店结果
 * @param {Array} hotel_data_list - 酒店数据列表
 * @param {boolean} use_table - 是否使用表格格式
 * @param {boolean} use_plain_link - 是否使用纯文本链接（转发给底层格式化函数）
 */
function format_hotel_result(hotel_data_list, use_table = false, use_plain_link = false) {
  if (!hotel_data_list || hotel_data_list.length === 0) {
    return '';
  }

  let output = '🏨 **推荐酒店**\n\n';

  hotel_data_list.forEach((item) => {
    if (item.hotelList && item.hotelList.length > 0) {
      output += format_hotel_table(item.hotelList, use_plain_link);
      output += '\n';
    }
  });

  return output;
}

/**
 * 格式化景区列表
 * @param {Array} scenery_data_list - 景区数据列表
 * @param {boolean} use_table - 是否使用表格格式
 * @param {boolean} use_plain_link - 是否使用纯文本链接（转发给底层格式化函数）
 */
function format_scenery_result(scenery_data_list, use_table = false, use_plain_link = false) {
  if (!scenery_data_list || scenery_data_list.length === 0) {
    return '';
  }

  // 任何一个景区数据的 needExtend 为 true 时，强制使用卡片格式
  const any_need_extend = scenery_data_list.some(item => item.needExtend);

  let output = '🏞️ **推荐景区/景点**\n\n';

  scenery_data_list.forEach((item) => {
    if (item.sceneryList && item.sceneryList.length > 0) {
      const sceneries = item.sceneryList;
      const need_extend = item.needExtend || false;
      if (use_table && !any_need_extend) {
        output += format_scenery_table(sceneries, use_plain_link);
      } else {
        sceneries.forEach((scenery) => {
          output += format_scenery_card(scenery, use_plain_link, need_extend);
        });
      }
      output += '\n';
    }
  });

  return output;
}

/**
 * 判断是否有有效的行程规划
 * @param {object} response_data - 解包后的业务数据
 * @returns {boolean} 是否有有效行程规划
 */
function has_valid_trip_plan(response_data) {
  const list = response_data?.tripPlanDataList;
  return Array.isArray(list) && list.length > 0;
}

/**
 * 将 UGC 数据列表扁平化为单层 ugc 条目数组
 * @param {Array} ugc_data_list - UGC 数据列表
 * @returns {Array} 扁平化后的 ugc 条目数组
 */
function flatten_ugc_list(ugc_data_list) {
  const all_ugcs = [];
  ugc_data_list.forEach((item) => {
    if (item.ugcList && item.ugcList.length > 0) {
      item.ugcList.forEach((ugc) => {
        all_ugcs.push(ugc);
      });
    }
  });
  return all_ugcs;
}

/**
 * 格式化 UGC 攻略详细内容（无行程规划时使用）
 * 输出 name、cityName、sceneryNameList、topic、ugcContent（摘要）等详细字段
 * @param {Array} ugc_data_list - UGC 数据列表
 * @returns {string} 格式化输出
 */
function format_ugc_guide_detail(ugc_data_list) {
  if (!ugc_data_list || ugc_data_list.length === 0) {
    return '';
  }

  const all_ugcs = flatten_ugc_list(ugc_data_list);

  if (all_ugcs.length === 0) {
    return '';
  }

  const CONTENT_SUMMARY_LIMIT = 2000;

  let output = '📝 **用户攻略推荐**（详细版）\n\n';
  output += `共找到 ${all_ugcs.length} 篇用户攻略，以下是详细内容：\n\n`;

  all_ugcs.forEach((ugc, idx) => {
    const name = ugc.name || '无标题';
    const author = ugc.nickName || '匿名用户';
    const city_name = ugc.cityName || '';
    const scenery_list = (ugc.sceneryNameList || []).filter(s => s && s !== '-');
    const topic = ugc.topic || '';
    const raw_content = ugc.ugcContent || '';
    const content_summary = raw_content.length > CONTENT_SUMMARY_LIMIT
      ? raw_content.substring(0, CONTENT_SUMMARY_LIMIT) + '…'
      : raw_content;
    const redirect_url = ugc.redirectUrl || '#';

    output += `${idx + 1}. **${name}** - ${author}\n`;
    if (city_name) {
      output += `   📍 城市：${city_name}\n`;
    }
    if (scenery_list.length > 0) {
      output += `   🏞️ 涉及景区：${scenery_list.join('、')}\n`;
    }
    if (topic) {
      output += `   🏷️ 话题：${topic}\n`;
    }
    if (content_summary) {
      output += `   📄 内容摘要：${content_summary}\n`;
    }
    output += `   🔗 [查看全文](${redirect_url})\n\n`;
  });

  output += '💡 以上攻略由真实用户分享，以下内容可作为你制定行程的参考。\n\n';

  return output;
}

/**
 * 格式化 UGC 攻略指引
 */
function format_ugc_guide(ugc_data_list) {
  if (!ugc_data_list || ugc_data_list.length === 0) {
    return '';
  }

  const all_ugcs = flatten_ugc_list(ugc_data_list);

  if (all_ugcs.length === 0) {
    return '';
  }

  let output = '📝 **用户攻略推荐**\n\n';
  output += `共找到 ${all_ugcs.length} 篇用户攻略，以下是推荐：\n\n`;

  all_ugcs.forEach((ugc, idx) => {
    const name = ugc.name || '无标题';
    const author = ugc.nickName || '匿名用户';
    const redirect_url = ugc.redirectUrl || '#';
    
    output += `${idx + 1}. **${name}** - ${author}\n`;
    output += `   🔗 [查看全文](${redirect_url})\n\n`;
  });

  output += '💡 以上攻略由真实用户分享，可供参考。\n\n';

  return output;
}

/**
 * 格式化补偿查询提示（无行程规划时输出）
 * @param {object} request_params - 原始请求参数
 * @param {object} response_data - 解包后的业务数据
 * @returns {string} 提示文案
 */
function format_compensation_hint(request_params, response_data) {
  const missing = [];
  const has_hotel = Array.isArray(response_data?.hotelDataList) && response_data.hotelDataList.length > 0;
  const has_scenery = Array.isArray(response_data?.sceneryDataList) && response_data.sceneryDataList.length > 0;
  const has_train = Array.isArray(response_data?.trainDataList) && response_data.trainDataList.length > 0;
  const has_flight = Array.isArray(response_data?.flightDataList) && response_data.flightDataList.length > 0;
  const has_bus = Array.isArray(response_data?.busDataList) && response_data.busDataList.length > 0;
  const has_traffic = has_train || has_flight || has_bus;

  if (!has_hotel) missing.push('酒店推荐');
  if (!has_scenery) missing.push('景区推荐');
  if (!has_traffic) missing.push('交通方式');

  if (missing.length === 0) {
    return '';
  }

  const destination = request_params?.destination || '';
  const extra = request_params?.extra || '';
  const departure = request_params?.departure || '';
  const channel = request_params?.channel || 'webchat';
  const surface = request_params?.surface || 'webchat';

  const extra_arg = extra ? ` --extra "${extra}"` : '';

  let output = '⚠️ 当前结果中缺少' + missing.join('、') + '，建议进一步调用以下查询获取更完整的行程参考：\n\n';

  if (!has_hotel) {
    output += `- hotel-query --destination "${destination}"${extra_arg} --channel ${channel} --surface ${surface}\n`;
  }
  if (!has_scenery) {
    output += `- scenery-query --destination "${destination}"${extra_arg} --channel ${channel} --surface ${surface}\n`;
  }
  if (!has_traffic) {
    if (departure) {
      output += `- traffic-query --departure "${departure}" --destination "${destination}"${extra_arg} --channel ${channel} --surface ${surface}\n`;
    } else {
      output += `- traffic-query --departure "出发地" --destination "${destination}"${extra_arg} --channel ${channel} --surface ${surface}\n`;
      output += `  ↑ 请先询问用户想从哪里出发\n`;
    }
  }

  output += '\n';

  return output;
}

/**
 * 处理查询结果
 */
function handle_result(response_data, { print_success_once, format_options, print_no_match, request_params }) {
  const { use_table, use_plain_link } = format_options;

  let has_output = false;
  let output_parts = [];

  const has_plan = has_valid_trip_plan(response_data);

  // 1. 火车票推荐（往返交通）
  const train_data_list = response_data?.trainDataList;
  if (Array.isArray(train_data_list) && train_data_list.length > 0) {
    const train_output = format_train_result(train_data_list, use_table, use_plain_link);
    if (train_output) {
      print_success_once();
      output_parts.push(train_output);
      has_output = true;
    }
  }

  // 2. 酒店推荐
  const hotel_data_list = response_data?.hotelDataList;
  if (Array.isArray(hotel_data_list) && hotel_data_list.length > 0) {
    const hotel_output = format_hotel_result(hotel_data_list, use_table, use_plain_link);
    if (hotel_output) {
      print_success_once();
      output_parts.push(hotel_output);
      has_output = true;
    }
  }

  // 3. 景区推荐（丰富行程规划）
  const scenery_data_list = response_data?.sceneryDataList;
  if (Array.isArray(scenery_data_list) && scenery_data_list.length > 0) {
    const scenery_output = format_scenery_result(scenery_data_list, use_table, use_plain_link);
    if (scenery_output) {
      print_success_once();
      output_parts.push(scenery_output);
      has_output = true;
    }
  }

  // 4. 传统打包产品（跟团游等）
  const trip_data_list = response_data?.tripDataList;
  if (Array.isArray(trip_data_list) && trip_data_list.length > 0) {
    trip_data_list.forEach((item, index) => {
      if (item.tripList && item.tripList.length > 0) {
        print_success_once();
        let part_output = '';
        if (item.desc) {
          part_output += `📌 ${item.desc}\n`;
        } else if (trip_data_list.length > 1) {
          part_output += `📌 列表 ${index + 1}\n`;
        }
        part_output += format_travel_result(item, use_table, use_plain_link);
        output_parts.push(part_output);
        has_output = true;
      }
    });
  }

  // 5. 行程规划（核心）
  if (has_plan) {
    const trip_plan_data_list = response_data?.tripPlanDataList;
    const plan_output = format_trip_plans(trip_plan_data_list, use_plain_link);
    if (plan_output) {
      print_success_once();
      output_parts.push(plan_output);
      has_output = true;
    }
  }

  // 6. UGC 攻略指引
  const ugc_data_list = response_data?.ugcDataList;
  if (Array.isArray(ugc_data_list) && ugc_data_list.length > 0) {
    let ugc_output;
    if (has_plan) {
      // 有行程规划时，UGC 仅输出简要信息
      ugc_output = format_ugc_guide(ugc_data_list);
    } else {
      // 无行程规划时，UGC 输出详细内容
      ugc_output = format_ugc_guide_detail(ugc_data_list);
    }
    if (ugc_output) {
      output_parts.push(ugc_output);
    }
  }

  // 7. 无行程规划时的补偿查询提示
  if (!has_plan) {
    const compensation_hint = format_compensation_hint(request_params, response_data);
    if (compensation_hint) {
      output_parts.push(compensation_hint);
    }
  }

  // 输出所有内容
  if (has_output) {
    output_parts.forEach((part) => {
      console.log(part);
    });
    console.log(MORE_CHOICES_PROMPT);
  } else {
    print_no_match();
  }
}

// 创建查询运行器
const runner = create_query_runner({
  api_path: TRAVEL_API_PATH,
  param_defs: {
    departure: '',
    destination: '',
    extra: '',
    channel: '',
    surface: ''
  },
  validate: validate_params,
  handle_result: handle_result,
  no_match_detail: NO_MATCH_DETAIL.TRAVEL,
  usage_example: `  node travel-query.js --destination "三亚"
  node travel-query.js --departure "北京" --destination "三亚"
  node travel-query.js --departure "北京" --destination "三亚" --extra "五一假期"`
});

// 导出函数供其他模块使用
module.exports = {
  validate_params,
  format_travel_result
};

// 运行主函数
if (require.main === module) {
  runner.run();
}
