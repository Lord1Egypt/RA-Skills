#!/usr/bin/env node

/**
 * 同程程心 API - 格式化器模块
 * 
 * 提供通用的格式化函数
 */

/**
 * 是否为有效预订链接（排除空串与占位 `#`）
 * @param {string} [url]
 * @returns {boolean}
 */
function is_valid_booking_url(url) {
  if (url == null || url === '') return false;
  const s = String(url).trim();
  return Boolean(s && s !== '#');
}

/**
 * 提取预订链接（PC 端 + 移动端）
 * @param {object} item - 含 pcRedirectUrl / clawRedirectUrl / redirectUrl 的数据对象
 * @returns {{ pc_link: string, mobile_link: string }}
 */
function extract_booking_links(item) {
  return {
    pc_link: item.pcRedirectUrl || '',
    mobile_link: item.clawRedirectUrl || item.redirectUrl || '',
  };
}

/**
 * 在机场名后追加航站楼（仅当航站楼非空时）
 * @param {string} airport_name - 机场名（如 "上海浦东国际机场"）
 * @param {string} [terminal] - 航站楼（如 "T2"，空串时不追加）
 * @returns {string} - 如 "上海浦东国际机场T2" 或 "北京大兴国际机场"
 */
function append_terminal(airport_name, terminal) {
  if (terminal && String(terminal).trim()) {
    return `${airport_name}${String(terminal).trim()}`;
  }
  return airport_name;
}

/**
 * 格式化时间（含日期和跨天标注）
 * @param {string} time - 时间（如 "07:50"）
 * @param {string} [date] - 日期（如 "2026-04-17"，取月日部分）
 * @param {string|number} [day_span] - 跨天标识（"0"/0=不跨天，"1"/1=跨1天）
 * @returns {string} - 如 "04-17 07:50"、"09:45+1天" 或 "07:50"
 */
function format_time_with_date(time, date, day_span) {
  if (!time) return '-';
  let result = '';
  // 有日期时在时间前加月日前缀
  if (date && String(date).length >= 10) {
    const md = String(date).slice(5, 10); // "04-17"
    result = `${md} ${time}`;
  } else {
    result = time;
  }
  // 跨天标注
  if (day_span != null && Number(day_span) > 0) {
    result += `+${Number(day_span)}天`;
  }
  return result;
}

/**
 * 渲染预订按钮（表格单元格与卡片共用）
 * @param {string} pc_link - PC 端链接
 * @param {string} mobile_link - 移动端链接
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 格式化后的按钮
 */
function render_booking_buttons(pc_link, mobile_link, use_plain_link = false) {
  const pc_ok = is_valid_booking_url(pc_link);
  const mob_ok = is_valid_booking_url(mobile_link);
  if (!pc_ok && !mob_ok) {
    return '';
  }

  if (use_plain_link) {
    const links = [];
    if (pc_ok) links.push(`🔗 PC 端：${pc_link}`);
    if (mob_ok) links.push(`🔗 移动端：${mobile_link}`);
    return links.join(' | ');
  }

  const buttons = [];
  if (pc_ok) buttons.push(`🔗 [PC 端预订](${pc_link})`);
  if (mob_ok) buttons.push(`🔗 [移动端预订](${mobile_link})`);
  return buttons.join('  ');
}

/**
 * 格式化火车坐席价格信息（从 ticketList 提取 ticketType + ticketPrice）
 * 将所有坐席和价格组合为一个字符串，用逗号分隔
 * @param {object} train - 火车数据（含 ticketList 数组）
 * @param {string|number} train.price - 最低价兜底
 * @returns {string} - 如 "二等座¥553, 一等座¥933" 或 "¥553"（无 ticketList 时兜底）
 */
function format_train_seat_prices(train) {
  if (Array.isArray(train.ticketList) && train.ticketList.length > 0) {
    const parts = train.ticketList
      .filter(t => t.ticketType && t.ticketPrice != null)
      .map(t => `${t.ticketType}¥${t.ticketPrice}`);
    if (parts.length > 0) return parts.join(', ');
  }
  // 兜底：使用原有 price 字段
  return train.price ? `¥${train.price}` : '暂无价格';
}

/**
 * 格式化时长（分钟 → 人类可读）
 * @param {number} minutes - 分钟数
 * @returns {string} - 格式化后的时长
 */
function format_duration(minutes) {
  if (!minutes || minutes <= 0) return '-';
  if (minutes >= 10080) {
    // 超过 7 天才显示天数，显示到天时不再显示分钟
    const days = Math.floor(minutes / 1440);
    const remain_minutes = minutes % 1440;
    const remain_hours = Math.floor(remain_minutes / 60);
    return remain_hours > 0 ? `${days}天${remain_hours}时` : `${days}天`;
  }
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  if (hours > 0) {
    return mins > 0 ? `${hours}时${mins}分` : `${hours}时`;
  }
  return `${mins}分`;
}

/**
 * 格式化中转联程行程（每段行程）
 * 统一班次号字段为 trafficNo；兼容旧版 trainCode、flightNo。
 * segmentType：TRAIN 为火车；FLIGHT、AIR 为航班；BUS 为汽车；缺省时按航班展示。
 * @param {object} segment - 行程段
 * @param {number} index - 序号
 * @returns {string} - 格式化输出
 */
function format_transfer_segment(segment, index) {
  const segment_type = segment.segmentType || '';
  const is_train = segment_type === 'TRAIN';
  const is_bus = segment_type === 'BUS';
  const is_flight = !is_train && !is_bus; // FLIGHT、AIR 或缺省均视为航班
  // BUS 展示为汽车；FLIGHT、AIR 或非 TRAIN/非 BUS 均展示为航班
  const type_icon = is_train ? '🚄' : (is_bus ? '🚌' : '✈️');
  const type_name = is_train ? '火车' : (is_bus ? '汽车' : '飞机');
  const traffic_no =
    segment.trafficNo != null && segment.trafficNo !== ''
      ? segment.trafficNo
      : segment.trainCode || segment.flightNo || '-';
  // 航班段：机场名追加航站楼；火车/汽车：仅用站名
  const dep_station = is_flight
    ? append_terminal(segment.depStationName || '-', segment.depAirportTerminal)
    : (segment.depStationName || '-');
  const arr_station = is_flight
    ? append_terminal(segment.arrStationName || '-', segment.arrAirportTerminal)
    : (segment.arrStationName || '-');
  // 航班段：时间含日期和跨天标注
  const dep_time = is_flight
    ? format_time_with_date(segment.depTime, segment.depDate, segment.daySpan)
    : (segment.depTime || '-');
  const arr_time = is_flight
    ? format_time_with_date(segment.arrTime, segment.arrDate, segment.daySpan)
    : (segment.arrTime || '-');
  const run_time_minutes = segment.runTimeMinutes || 0;
  const run_time = format_duration(run_time_minutes);
  const seat_name = segment.seatName || '-';
  // segment.price：中转段总价，由 API 在 segmentList 中直接返回；
  // 与火车直达的 ticketList[].ticketPrice 不同（直达价格在 ticketList 中逐席别列出）
  const price = segment.price ? `¥${segment.price}` : '-';
  
  let output = `| 第${index}程 | ${type_icon}${type_name} | ${traffic_no} | ${dep_station} | ${arr_station} | ${dep_time} | ${arr_time} | ${run_time} | ${seat_name} | ${price} |`;
  
  return output;
}

/**
 * 格式化中转信息
 * @param {object} transfer_info - 中转信息
 * @returns {string} - 格式化输出
 */
function format_transfer_info(transfer_info) {
  const city = transfer_info.transferCityName || '未知城市';
  const interval = transfer_info.intervalTimeDesc || '未知时长';
  return `📍 **中转：${city}** (等待 ${interval})\n`;
}

/**
 * 格式化机票结果（卡片格式）
 * @param {object} flight - 航班数据
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 格式化输出
 */
function format_flight_card(flight, use_plain_link = false) {
  const flight_no = flight.flightNo || '-';
  const airline = flight.airlineName || '-';
  const dep_airport = append_terminal(flight.depAirportName || '-', flight.depAirportTerminal);
  const arr_airport = append_terminal(flight.arrAirportName || '-', flight.arrAirportTerminal);
  const dep_time = format_time_with_date(flight.depTime, flight.depDate, flight.daySpan);
  const arr_time = format_time_with_date(flight.arrTime, flight.arrDate, flight.daySpan);
  const run_time = flight.runTime || '-';
  const price = flight.price ? `¥${flight.price}` : '暂无价格';
  
  // 构建链接：仅使用航班独立的 pcRedirectUrl，无兜底
  const { pc_link, mobile_link } = extract_booking_links(flight);
  
  let output = `### ✈️ ${flight_no} | ${dep_airport} → ${arr_airport}\n`;
  output += `**出发时间** ${dep_time} | **到达时间** ${arr_time} | **时长** ${run_time}\n`;
  output += `**价格** ${price}\n`;
  output += `**航司** ${airline}\n`;
  output += render_booking_buttons(pc_link, mobile_link, use_plain_link) + "\n";
  output += '\n---\n\n';
  
  return output;
}

/**
 * 格式化酒店卡片
 * @param {object} hotel - 酒店数据
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 格式化输出
 */
function format_hotel_card(hotel, use_plain_link = false) {
  const name = hotel.name || '未知酒店';
  const price = hotel.price ? `¥${hotel.price}` : '暂无价格';
  const star = hotel.star || '未评级';
  const score = hotel.score || '暂无';
  const comment_num = hotel.commentNum || '0';
  const describe = hotel.describe || '';
  const address = hotel.address || '';
  const county = hotel.countyName || '';
  const brand = hotel.brandName || '';
  const facilities = hotel.facilities || '';
  const distance = hotel.distance || '';
  const recommend_reasons = hotel.recommendReasons || '';

  const { pc_link, mobile_link } = extract_booking_links(hotel);

  let output = `### 🏨 ${name}\n`;
  output += `**价格** ${price} | **星级** ${star} | **评分** ⭐${score}（${comment_num}条）\n`;
  if (brand) output += `**品牌** ${brand}\n`;
  if (facilities) output += `**设施** ${facilities}\n`;
  if (distance) output += `**距离** ${distance}\n`;
  if (recommend_reasons) output += `**推荐理由** ${recommend_reasons}\n`;
  if (describe) output += `**特色** ${describe}\n`;
  const full_address = county ? `${county} · ${address}` : address;
  if (full_address) output += `**地址** ${full_address}\n`;
  output += render_booking_buttons(pc_link, mobile_link, use_plain_link) + "\n";
  output += '\n---\n\n';

  return output;
}

/**
 * 站名标注城市：站名有效且不含城市前缀时追加 (城市)
 * @param {string} station - 站名
 * @param {string} [city] - 城市名
 * @returns {string} - 如 "南门汽车站(苏州)" 或 "苏州北广场汽车客运站"
 */
function label_station_with_city(station, city) {
  if (!city || station === '-') return station;
  return station.startsWith(city) ? station : `${station}(${city})`;
}

/**
 * 格式化汽车票卡片（bus-query.js 使用，字段丰富）
 * @param {object} bus - 汽车票数据
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 格式化输出
 */
function format_bus_card(bus, use_plain_link = false) {
  // 车次号：兼容 coachNo（新）与 busNo/busName（旧）
  const bus_no = bus.coachNo || bus.busNo || bus.busName || '-';
  // 车站：兼容新字段 depStationName/arrStationName 与旧字段 depName/arrName
  const dep_station = bus.depStationName || bus.depName || '-';
  const arr_station = bus.arrStationName || bus.arrName || '-';
  const dep_time = bus.depTime || '-';
  // 时长：优先用 format_duration 转换 runTimeMinutes，其次用 runTimeDesc，最后用 runTime
  const run_time_minutes = bus.runTimeMinutes || 0;
  const run_time = run_time_minutes > 0 ? format_duration(run_time_minutes) : (bus.runTimeDesc || bus.runTime || '-');
  // 车型（新字段）
  const coach_type = bus.coachType || '';
  // 价格
  const price = bus.price ? `¥${bus.price}` : '暂无价格';

  // 链接：优先用 clawRedirectUrl，兼容 redirectUrl
  const { pc_link, mobile_link } = extract_booking_links(bus);

  // 站名标注城市
  const dep_city = bus.depCityName || '';
  const arr_city = bus.arrCityName || '';
  const route_header = `${label_station_with_city(dep_station, dep_city)} → ${label_station_with_city(arr_station, arr_city)}`;
  
  let output = `### 🚌 ${bus_no} | ${route_header}\n`;
  output += `**出发** ${dep_time} | **时长** ${run_time}\n`;
  output += `**价格** ${price}`;
  if (coach_type) output += ` | **车型** ${coach_type}`;
  output += `\n`;
  output += render_booking_buttons(pc_link, mobile_link, use_plain_link) + "\n";
  output += '\n---\n\n';
  
  return output;
}

/**
 * 格式化景区门票卡片
 * @param {object} scenery - 景区数据
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @param {boolean} needExtend - 是否包含扩展信息（交通/票务/优惠等）
 * @returns {string} - 格式化输出
 */
function format_scenery_card(scenery, use_plain_link = false, needExtend = false) {
  const name = scenery.name || '未知景区';
  const city = scenery.cityName || '-';
  const star = scenery.star || '未评级';
  const score = scenery.score || '暂无';
  const comment_num = scenery.commentNum || '0';
  const price = scenery.price ? `¥${scenery.price}` : '暂无价格';
  const open_time = scenery.openTime || '未公布';
  const describe = scenery.describe || '';
  const play_time = scenery.playTime || '';

  // 常规渲染字段（table/card 均展示）
  const rank_title = scenery.rankTitle || '';
  const hot_topic = scenery.hotTopic || '';
  const best_play_time = scenery.bestPlayTime || '';
  const facility_list = scenery.facilityList || [];
  
  const { pc_link, mobile_link } = extract_booking_links(scenery);
  
  let output = `### 🏞️ ${name}\n`;
  if (rank_title) output += `🏅 ${rank_title}\n`;
  output += `**城市** ${city} | **星级** ${star} | **评分** ⭐${score}（${comment_num}条）\n`;
  output += `**门票** ${price} | **开放时间** ${open_time}\n`;
  if (play_time) output += `**建议游玩** ${play_time}\n`;
  if (describe) output += `**特点** ${describe}\n`;
  if (best_play_time) output += `**最佳游玩时间** ${best_play_time}\n`;
  if (hot_topic) output += `**热门话题** ${hot_topic}\n`;
  if (facility_list.length > 0) output += `**设施** ${facility_list.join('、')}\n`;

  // needExtend=true 时的扩展字段
  if (needExtend) {
    const warm_tips = scenery.warmTips || '';
    const introduce_list = scenery.introduceList || [];
    const preferential_policy = scenery.preferentialPolicy || '';
    const traffic_list = scenery.trafficList || [];
    const ticket_entity_list = scenery.ticketEntityList || [];

    if (traffic_list.length > 0) {
      const valid_traffic = traffic_list.filter(t => t.value && t.value.trim());
      if (valid_traffic.length > 0) {
        output += `\n**🚌 交通指引**\n`;
        valid_traffic.forEach(t => {
          output += `- ${t.key}：${t.value.replace(/\n/g, ' ')}\n`;
        });
      }
    }

    if (ticket_entity_list.length > 0) {
      output += `\n**🎫 票务信息**\n`;
      ticket_entity_list.forEach(t => {
        output += `- ${t.productName}：¥${t.amount}`;
        if (t.getTicketMode && t.getTicketMode.getTicketShortDesc) {
          output += ` | ${t.getTicketMode.getTicketShortDesc}`;
        }
        output += '\n';
      });
    }

    if (preferential_policy) {
      output += `\n**💡 优惠政策**\n${preferential_policy}\n`;
    }

    if (introduce_list.length > 0) {
      output += `\n**📖 景区介绍**\n`;
      introduce_list.forEach((text, i) => {
        output += `${i + 1}. ${text}\n`;
      });
    }

    if (warm_tips) {
      output += `\n**⚠️ 温馨提示**\n${warm_tips}\n`;
    }
  }

  output += render_booking_buttons(pc_link, mobile_link, use_plain_link) + "\n";
  output += '\n---\n\n';
  
  return output;
}

/**
 * 格式化交通方案卡片
 * @param {object} traffic - 交通方案数据
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 格式化输出
 */
function format_traffic_card(traffic, use_plain_link = false) {
  const type = traffic.type || '未知';
  const name = traffic.name || '-';
  const dep_station = traffic.depStationName || '-';
  const arr_station = traffic.arrStationName || '-';
  const dep_time = traffic.depTime || '-';
  const arr_time = traffic.arrTime || '-';
  const run_time = traffic.runTime || '-';
  const price = traffic.price ? `¥${traffic.price}` : '暂无价格';
  
  const { pc_link, mobile_link } = extract_booking_links(traffic);
  
  let output = `### ${type} ${name}\n`;
  output += `**出发** ${dep_station} ${dep_time} | **到达** ${arr_station} ${arr_time}\n`;
  output += `**时长** ${run_time} | **价格** ${price}\n`;
  output += render_booking_buttons(pc_link, mobile_link, use_plain_link) + "\n";
  output += '\n---\n\n';
  
  return output;
}

/**
 * 格式化度假产品卡片
 * @param {object} trip - 度假产品数据
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 格式化输出
 */
function format_trip_card(trip, use_plain_link = false) {
  const name = trip.name || '未知产品';
  const price = trip.price ? `¥${trip.price}` : '暂无价格';
  const desc = trip.desc || trip.describe || '';
  const address = trip.address || '';
  
  const { pc_link, mobile_link } = extract_booking_links(trip);
  
  let output = `### 🏖️ ${name}\n`;
  output += `**价格** ${price}\n`;
  if (desc) output += `**特色** ${desc}\n`;
  if (address) output += `**地址** ${address}\n`;
  output += render_booking_buttons(pc_link, mobile_link, use_plain_link) + "\n";
  output += '\n---\n\n';
  
  return output;
}

/**
 * 格式化火车卡片
 * @param {object} train - 火车数据
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 格式化输出
 */
function format_train_card(train, use_plain_link = false) {
  const train_no = train.trainType === 'GD' ? `🚅 ${train.trainNo}` : `🚆 ${train.trainNo}`;
  const dep_station = train.depStationName || '-';
  const arr_station = train.arrStationName || '-';
  const dep_time = train.depTime || '-';
  const arr_time = train.arrTime || '-';
  const run_time = train.runTime || '-';
  const seat_prices = format_train_seat_prices(train);

  const { pc_link, mobile_link } = extract_booking_links(train);
  
  let output = `### ${train_no} | ${dep_station} → ${arr_station}\n`;
  output += `**出发时间** ${dep_time} | **到达时间** ${arr_time} | **时长** ${run_time}\n`;
  output += `**价格** ${seat_prices}\n`;
  output += render_booking_buttons(pc_link, mobile_link, use_plain_link) + "\n";
  output += '\n---\n\n';
  
  return output;
}

/**
 * 格式化航班表格（常规航班）
 * @param {Array} flights - 航班列表
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 表格输出
 */
function format_flight_table(flights, use_plain_link = false) {
  if (!flights || flights.length === 0) return '';
  
  let output = '| 航班号 | 出发机场 | 到达机场 | 出发时间 | 到达时间 | 时长 | 价格 | 航司 | 预订 |\n';
  output += '|--------|---------|---------|---------|---------|------|------|------|--------|\n';
  
  flights.forEach((flight) => {
    const flight_no = flight.flightNo || '-';
    const airline = flight.airlineName || '-';
    const dep_airport = append_terminal(flight.depAirportName || '-', flight.depAirportTerminal);
    const arr_airport = append_terminal(flight.arrAirportName || '-', flight.arrAirportTerminal);
    const dep_time = format_time_with_date(flight.depTime, flight.depDate, flight.daySpan);
    const arr_time = format_time_with_date(flight.arrTime, flight.arrDate, flight.daySpan);
    const run_time = flight.runTime || '-';
    const price = flight.price ? `¥${flight.price}` : '暂无价格';
    const { pc_link, mobile_link } = extract_booking_links(flight);
    
    output += `| ${flight_no} | ${dep_airport} | ${arr_airport} | ${dep_time} | ${arr_time} | ${run_time} | ${price} | ${airline} | ${render_booking_buttons(pc_link, mobile_link, use_plain_link)} |\n`;
  });

  output += '\n';
  return output;
}

/**
 * 格式化特价机票表格
 * @param {Array} flights - 特价航班列表（flightNo 为 null/undefined）
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 表格输出
 */
function format_flight_table_special(flights, use_plain_link = false) {
  if (!flights || flights.length === 0) return '';
  
  let output = '| 目的地 | 价格 | 日期 | 折扣 | 原价 | 预订链接 |\n';
  output += '|--------|------|------|------|------|----------|\n';
  
  flights.forEach((flight) => {
    const dep_name = flight.depName || '-';
    const arr_name = flight.arrName || '-';
    const price = flight.price ? `¥${flight.price}` : '暂无价格';
    const week = flight.week || '-';
    const discount = flight.discount || '-';
    const origin_price = flight.originPrice ? `¥${flight.originPrice}` : '-';
    const { pc_link, mobile_link } = extract_booking_links(flight);
    
    output += `| ${dep_name}→${arr_name} | ${price} | ${week} | ${discount} | ${origin_price} | ${render_booking_buttons(pc_link, mobile_link, use_plain_link)} |\n`;
  });

  output += '\n';
  return output;
}

/**
 * 格式化度假产品表格
 * @param {Array} trips - 度假产品列表
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 表格输出
 */
function format_trip_table(trips, use_plain_link = false) {
  if (!trips || trips.length === 0) return '';
  
  let output = '| 产品 | 目的地 | 价格 | 评分 | 特点 | 预订 |\n';
  output += '|------|--------|------|------|------|--------|\n';
  
  trips.forEach((trip) => {
    const name = trip.name || '未知产品';
    const dest_list = (trip.destList || []).join(', ');
    const price = trip.price ? `¥${trip.price}` : '暂无价格';
    const score = trip.score && trip.score !== '0.0' ? `⭐${trip.score}` : '暂无';
    const label_list = (trip.labelList || []).join(', ');
    
    // 跟团游只有 redirectUrl（手机端），可能无 pcRedirectUrl
    const { pc_link, mobile_link } = extract_booking_links(trip);
    
    output += `| ${name} | ${dest_list} | ${price} | ${score} | ${label_list} | ${render_booking_buttons(pc_link, mobile_link, use_plain_link)} |\n`;
  });

  output += '\n';
  return output;
}

/**
 * 格式化景区表格
 * @param {Array} sceneries - 景区列表
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 表格输出
 */
function format_scenery_table(sceneries, use_plain_link = false) {
  if (!sceneries || sceneries.length === 0) return '';
  
  let output = '| 景区名称 | 城市 | 门票 | 评分 | 开放时间 | 榜单 | 最佳游玩 | 设施 | 预订 |\n';
  output += '|----------|------|------|------|----------|------|----------|------|--------|\n';
  
  sceneries.forEach((scenery) => {
    const name = scenery.name || '未知景区';
    const city = scenery.cityName || '-';
    const price = scenery.price ? `¥${scenery.price}` : '暂无价格';
    const score = scenery.score || '暂无';
    const comment_num = scenery.commentNum || '0';
    const open_time = scenery.openTime || '未公布';
    const rank_title = scenery.rankTitle || '-';
    const best_play_time = scenery.bestPlayTime || '-';
    const facility_list = (scenery.facilityList || []).join('、') || '-';
    
    const { pc_link, mobile_link } = extract_booking_links(scenery);
    
    output += `| ${name} | ${city} | ${price} | ⭐${score}（${comment_num}条） | ${open_time} | ${rank_title} | ${best_play_time} | ${facility_list} | ${render_booking_buttons(pc_link, mobile_link, use_plain_link)} |\n`;
  });

  output += '\n';
  return output;
}

/**
 * 格式化酒店表格
 * @param {Array} hotels - 酒店列表
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 表格输出
 */
function format_hotel_table(hotels, use_plain_link = false) {
  if (!hotels || hotels.length === 0) return '';

  let output = '| 酒店名称 | 价格 | 类型 | 评分 | 距离 | 品牌 | 设施 | 推荐理由 | 地址 | 预订 |\n';
  output += '|----------|------|------|------|------|------|------|----------|------|--------|\n';

  hotels.forEach((hotel) => {
    const name = hotel.name || '未知酒店';
    const price = hotel.price ? `¥${hotel.price}` : '暂无价格';
    const star = hotel.star || '未评级';
    const score = hotel.score || '暂无';
    const comment_num = hotel.commentNum || '0';
    const address = hotel.address || '';
    const county = hotel.countyName || '';
    const distance = hotel.distance || '';
    const brand = hotel.brandName || '';
    const facilities = hotel.facilities || '';
    const recommend_reasons = hotel.recommendReasons || '';
    const { pc_link, mobile_link } = extract_booking_links(hotel);

    const full_address = county ? `${county} · ${address}` : address;
    output += `| ${name} | ${price} | ${star} | ⭐${score}（${comment_num}条） | ${distance || '-'} | ${brand || '-'} | ${facilities || '-'} | ${recommend_reasons || '-'} | ${full_address} | ${render_booking_buttons(pc_link, mobile_link, use_plain_link)} |\n`;
  });

  output += '\n';
  return output;
}

/**
 * 格式化汽车票表格（bus-query.js / traffic-query.js 共用）
 * @param {Array} buses - 汽车票列表
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 表格输出
 */
function format_bus_table(buses, use_plain_link = false) {
  if (!buses || buses.length === 0) return '';

  let output = '| 班次 | 车型 | 出发站 | 到达站 | 出发时间 | 时长 | 价格 | 预订 |\n';
  output += '|------|------|--------|--------|---------|------|------|--------|\n';

  buses.forEach((bus) => {
    const bus_no = bus.coachNo || bus.busNo || bus.busName || '-';
    const coach_type = bus.coachType || '-';
    const dep_station = bus.depStationName || bus.depName || '-';
    const arr_station = bus.arrStationName || bus.arrName || '-';
    const dep_city = bus.depCityName || '';
    const arr_city = bus.arrCityName || '';
    const dep_time = bus.depTime || '-';
    const run_time_minutes = bus.runTimeMinutes || 0;
    const run_time = run_time_minutes > 0 ? format_duration(run_time_minutes) : (bus.runTimeDesc || bus.runTime || '-');
    const price = bus.price ? `¥${bus.price}` : '暂无价格';
    const { pc_link, mobile_link } = extract_booking_links(bus);

    output += `| ${bus_no} | ${coach_type} | ${label_station_with_city(dep_station, dep_city)} | ${label_station_with_city(arr_station, arr_city)} | ${dep_time} | ${run_time} | ${price} | ${render_booking_buttons(pc_link, mobile_link, use_plain_link)} |\n`;
  });

  output += '\n';
  return output;
}

/**
 * 格式化火车表格（直达车次）
 * @param {Array} trains - 火车列表
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 表格输出
 */
function format_train_table(trains, use_plain_link = false) {
  if (!trains || trains.length === 0) return '';
  
  let output = '| 车次 | 出发站 | 到达站 | 出发时间 | 到达时间 | 运行时长 | 价格 | 预订 |\n';
  output += '|------|--------|--------|---------|---------|---------|------|--------|\n';
  
  trains.forEach((train) => {
    const train_no = train.trainType === 'GD' ? `🚅 ${train.trainNo}` : `🚆 ${train.trainNo}`;
    const dep_station = train.depStationName || '-';
    const arr_station = train.arrStationName || '-';
    const dep_time = train.depTime || '-';
    const arr_time = train.arrTime || '-';
    const run_time = train.runTime || '-';
    const seat_prices = format_train_seat_prices(train);
    
    const { pc_link, mobile_link } = extract_booking_links(train);
    
    output += `| ${train_no} | ${dep_station} | ${arr_station} | ${dep_time} | ${arr_time} | ${run_time} | ${seat_prices} | ${render_booking_buttons(pc_link, mobile_link, use_plain_link)} |\n`;
  });

  output += '\n';
  return output;
}

/**
 * 格式化中转联程方案（火车/机票/汽车票接口共用；顶层可为站名或机场名）
 * @param {object} trip - 中转联程数据
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 格式化输出
 */
function format_transfer_trip(trip, use_plain_link = false) {
  const dep_end = trip.depStationName || trip.depAirportName || '-';
  const arr_end = trip.arrStationName || trip.arrAirportName || '-';
  let output = `\n🔄 **中转联程：${dep_end} → ${arr_end}**\n`;
  output += `💰 **总价：¥${trip.price}** | ⏱️ **总时长：${trip.runTime}**\n\n`;
  
  // 每段行程一个小表格（班次号列为 trafficNo，含火车车次与航班号）
  output += '| 程次 | 类型 | 班次 | 出发站 | 到达站 | 出发时间 | 到达时间 | 时长 | 席别 | 价格 |\n';
  output += '|------|------|------|--------|--------|---------|---------|------|------|------|\n';
  
  if (trip.segmentList && trip.segmentList.length > 0) {
    trip.segmentList.forEach((segment, index) => {
      output += format_transfer_segment(segment, index + 1) + '\n';
    });
  }
  
  // 中转信息
  if (trip.transferInfoList && trip.transferInfoList.length > 0) {
    output += '\n';
    trip.transferInfoList.forEach((info) => {
      output += format_transfer_info(info);
    });
  }
  
  // 预订链接
  const { pc_link, mobile_link } = extract_booking_links(trip);
  
  output += `\n🔗 **立即预订**：${render_booking_buttons(pc_link, mobile_link, use_plain_link)}\n`;
  output += '\n---\n\n';
  
  return output;
}


/**
 * 渲染单个补偿交通表格
 * @param {Array} list - 交通段列表
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @param {number} max_items - 最多展示条数
 * @returns {string} - 表格输出
 */
function render_supplement_table(list, use_plain_link, max_items) {
  const limited = list.slice(0, max_items);

  let output = '| 班次 | 出发站 | 到达站 | 出发时间 | 时长 | 价格 | 席别 | 预订 |\n';
  output += '|------|--------|--------|---------|------|------|------|------|\n';

  limited.forEach((seg) => {
    const segment_type = seg.segmentType || '';
    const is_train = segment_type === 'TRAIN';
    const is_bus = segment_type === 'BUS';
    const type_icon = is_train ? '🚄' : (is_bus ? '🚌' : '🚄');
    const traffic_no = seg.trafficNo || '-';
    const dep_station = seg.depStationName || '-';
    const arr_station = seg.arrStationName || '-';
    // 优先使用分离的 depTime，其次从 depDateTime 提取
    const dep_time = seg.depTime || (seg.depDateTime ? seg.depDateTime.slice(11, 16) : '-');
    const run_time = seg.runTime || '-';
    const price = seg.price ? `¥${seg.price}` : '-';

    // 席别价格：取前 2 个席别简洁展示
    let seat_info = '';
    if (Array.isArray(seg.ticketList) && seg.ticketList.length > 0) {
      seat_info = seg.ticketList.slice(0, 2)
        .filter(t => t.ticketType && t.ticketPrice != null)
        .map(t => `${t.ticketType}¥${t.ticketPrice}`)
        .join(', ');
    }
    if (!seat_info && seg.seatName) {
      seat_info = seg.seatName;
    }

    const { pc_link, mobile_link } = extract_booking_links(seg);

    output += `| ${type_icon}${traffic_no} | ${dep_station} | ${arr_station} | ${dep_time} | ${run_time} | ${price} | ${seat_info || '-'} | ${render_booking_buttons(pc_link, mobile_link, use_plain_link)} |\n`;
  });

  if (list.length > max_items) {
    output += `\n> 还有 ${list.length - max_items} 趟可选，可在同程旅行 APP 中查看更多\n`;
  }

  output += '\n';
  return output;
}

/**
 * 格式化补偿交通数据（航班附加的前往/离开机场的交通推荐）
 * @param {object} item - flightDataList 中的单项（含 supplementDepartTrafficList + supplementDestTrafficList）
 * @param {boolean} [use_plain_link=false] - 是否使用纯文本链接
 * @param {number} [max_items=5] - 最多展示条数
 * @returns {string} - 格式化输出
 */
function format_supplement_traffic(item, use_plain_link = false, max_items = 5) {
  let output = '';

  // 首程接驳：前往出发机场
  const departList = item.supplementDepartTrafficList;
  if (Array.isArray(departList) && departList.length > 0) {
    output += '\n🚄 **前往出发机场的交通**\n\n';
    output += render_supplement_table(departList, use_plain_link, max_items);
  }

  // 尾程接驳：到达后前往目的地
  const destList = item.supplementDestTrafficList;
  if (Array.isArray(destList) && destList.length > 0) {
    output += '\n🚄 **到达后前往目的地的交通**\n\n';
    output += render_supplement_table(destList, use_plain_link, max_items);
  }

  return output;
}

/**
 * 格式化行程规划方案（单日）
 * @param {object} plan - 行程规划方案
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 格式化输出
 */
function format_trip_plan(plan, use_plain_link = false) {
  if (!plan || !plan.planList || plan.planList.length === 0) {
    return '';
  }

  let output = '';
  output += `📋 **行程概览**\n`;
  output += `⏱️ **天数**: ${plan.totalDays || '-'} 天`;
  output += ` | 🏨 **住宿**: ${plan.hotelNights || '-'} 晚`;
  output += ` | 🍜 **美食**: ${plan.foods || '暂无'}\n`;
  output += `🎯 **景点数**: ${plan.sceneryCount || '-'} 个\n\n`;

  output += `📅 **每日行程**\n\n`;

  plan.planList.forEach((day) => {
    const dayIndex = day.index || '?';
    const summary = day.summary || '无';
    const cities = day.cityNameList ? day.cityNameList.join('、') : '';

    output += `### Day ${dayIndex}：${summary}\n`;
    if (cities) {
      output += `📍 **城市**: ${cities}\n`;
    }

    // activitiyList：API 实际返回的字段名（缺 e）；activityList：兼容正确拼写
    const activity_list = day.activitiyList || day.activityList || [];
    if (activity_list.length > 0) {
      activity_list.forEach((activity, idx) => {
        const name = activity.name || '未知景点';
        const intro = activity.introduction || activity.describe || '';
        const { pc_link, mobile_link } = extract_booking_links(activity);

        output += `\n**${idx + 1}. ${name}**\n`;
        if (intro) {
          output += intro + '\n';
        }

        // 详细信息行：仅在有值时展示
        const detail_parts = [];
        if (activity.price !== undefined && activity.price !== null && activity.price !== '') {
          detail_parts.push(`**门票** ¥${String(activity.price)}`);
        }
        if (activity.star) {
          detail_parts.push(`**星级** ${String(activity.star)}`);
        }
        if (activity.score) {
          const comment_info = activity.commentNum ? `（${String(activity.commentNum)}条）` : '';
          detail_parts.push(`**评分** ⭐${String(activity.score)}${comment_info}`);
        }
        if (activity.openTime) {
          detail_parts.push(`**开放时间** ${String(activity.openTime)}`);
        }
        if (activity.playTime) {
          detail_parts.push(`**建议游玩** ${String(activity.playTime)}`);
        }
        if (activity.theme) {
          detail_parts.push(`**主题** ${String(activity.theme)}`);
        }
        if (detail_parts.length > 0) {
          output += detail_parts.join(' | ') + '\n';
        }

        output += '\n🔗 **立即预订**：' + render_booking_buttons(pc_link, mobile_link, use_plain_link) + '\n';
      });
    }

    output += '\n---\n\n';
  });

  return output;
}

/**
 * 格式化多个行程规划方案
 * @param {Array} plans - 行程规划方案列表
 * @param {boolean} use_plain_link - 是否使用纯文本链接
 * @returns {string} - 格式化输出
 */
function format_trip_plans(plans, use_plain_link = false) {
  if (!plans || plans.length === 0) {
    return '';
  }

  let output = '';
  output += '★★★★★ 以下为向你推荐的行程规划信息，你可以参考并预订每一天的行程 ★★★★★\n\n';
  output += '📋 **输出要求**：\n';
  output += '1. 完整输出所有行程规划方案，不要筛选、不要遗漏任何方案\n';
  output += '2. 每个方案必须包含完整的每日行程（Day 1, Day 2, ...），不要跳过任何一天\n';
  output += '3. 保留每个景点/活动的推荐理由和详细介绍，不要删减\n';
  output += '4. 保持原始预订链接格式，不要改写 URL\n';
  output += '5. 如果内容较长，可以分段输出，但必须确保完整性\n\n';
  output += '🗺️ **推荐行程规划**\n\n';

  plans.forEach((plan, index) => {
    if (plans.length > 1) {
      output += `#### 方案 ${index + 1}\n\n`;
    }
    output += format_trip_plan(plan, use_plain_link);
  });

  return output;
}

// ============================================================
// 公交地铁（transitRoute）格式化
// ============================================================

/**
 * 交通工具类型 → 图标 + 名称映射
 * @param {object} vehicle_info - vehicleInfo 对象
 * @returns {{ icon: string, name: string }}
 */
function resolve_vehicle_type(vehicle_info) {
  if (!vehicle_info) return { icon: '❓', name: '未知' };
  
  const v_type = vehicle_info.type;
  const detail = vehicle_info.detail || {};
  const d_type = detail.type;
  
  // type 3 时再区分公交/地铁
  if (v_type === 3) {
    if (d_type === 1) return { icon: '🚇', name: '地铁' };
    return { icon: '🚌', name: '公交' };
  }
  
  const type_map = {
    1: { icon: '🚄', name: '火车' },
    2: { icon: '✈️', name: '飞机' },
    4: { icon: '🚗', name: '驾车' },
    5: { icon: '🚶', name: '步行' },
    6: { icon: '🚌', name: '大巴' },
  };
  return type_map[v_type] || { icon: '❓', name: '未知' };
}

/**
 * 统计路线的换乘次数 = 非步行步骤数 - 1
 * @param {Array} steps - 展开后的一维步骤数组
 * @returns {number}
 */
function count_transfers(steps) {
  const non_walk_steps = steps.filter(s => {
    const st = s.stepType || '';
    return st !== 'walk' && s.vehicleInfo?.type !== 5;
  });
  return Math.max(0, non_walk_steps.length - 1);
}

/**
 * 格式化 transitRoute 价格
 * @param {number} price - 价格（-1.0 表示免费/未知）
 * @returns {string}
 */
function format_transit_price(price) {
  if (price == null || price < 0) return '免费';
  return `¥${price}`;
}

/**
 * 格式化 transitRoute 中的单个步骤
 * @param {object} step - 步骤数据
 * @param {number} index - 步骤序号（从 1 开始）
 * @returns {string} - 格式化后的步骤文本
 */
function format_transit_step(step, index) {
  const vehicle = resolve_vehicle_type(step.vehicleInfo);
  const detail = step.vehicleInfo?.detail || {};
  const step_type = step.stepType || '';
  
  // 步行特殊处理
  if (step_type === 'walk' || vehicle.name === '步行') {
    const dist = step.distance ? `${(step.distance / 1000).toFixed(1)}公里` : '';
    return `${index}. 🚶 步行 ${dist}`;
  }
  
  const line = `${index}. ${vehicle.icon} ${detail.name || ''}`;
  const direction = detail.directText ? `（${detail.directText}）` : '';
  const stations = detail.onStation && detail.offStation 
    ? ` ${detail.onStation} → ${detail.offStation}` : '';
  const stops = detail.stopNum ? ` | ${detail.stopNum}站` : '';
  
  // 首末班车
  const time_info = [];
  if (detail.firstTime) time_info.push(`首 ${detail.firstTime}`);
  if (detail.lastTime) time_info.push(`末 ${detail.lastTime}`);
  const schedule = time_info.length > 0 ? ` | ${time_info.join(' / ')}` : '';
  
  return `${line}${direction}${stations}${stops}${schedule}`;
}

/**
 * 格式化 transitRoute 数据（公交地铁）
 * 注意：小交通始终是卡片式展示，不受 use_table 控制。
 * 小交通是路线参考，不提供预订链接。
 * 
 * @param {object} transit_route - transitRoute 对象（含 origin, destination, routes, total）
 * @param {boolean} use_plain_link - 预留兼容（小交通无预订链接）
 * @returns {string} - 格式化输出
 */
function format_transit_route(transit_route, use_plain_link = false) {
  if (!transit_route || !Array.isArray(transit_route.routes) || transit_route.routes.length === 0) {
    return '';
  }
  
  // 起终点名称
  const depart_name = transit_route.routes[0]?.departName || '出发地';
  const dest_name = transit_route.routes[0]?.destName || '目的地';
  const total = transit_route.total || transit_route.routes.length;
  const max_show = 3; // 最多展示 3 条路线
  
  let output = `\n🚌 **公交地铁：${depart_name} → ${dest_name}**\n\n`;
  // 提示词：告知大模型这是路线参考，时间信息可能基于某个航班的到达时间给出建议
  output += '📋 **小交通路线参考**（以下路线信息基于你的行程时间给出建议，请结合实际情况安排出行。公交/地铁首末班时间仅供参考，建议以当地实际运营时间为准。）\n';
  
  transit_route.routes.slice(0, max_show).forEach((route, idx) => {
    const is_recommended = idx === 0;
    const duration = route.duration ? format_duration(Math.round(route.duration / 60)) : '-';
    const dist = route.distance ? `${(route.distance / 1000).toFixed(1)}公里` : '-';
    const price = format_transit_price(route.price);
    
    // 展开 steps（二维数组 → 一维）
    const flat_steps = (route.steps || []).flatMap(group => 
      Array.isArray(group) ? group : [group]
    );
    const transfers = count_transfers(flat_steps);
    
    output += `### 方案 ${idx + 1}${is_recommended ? '（推荐）' : ''}\n`;
    output += `⏱️ **${duration}** | 📏 **${dist}** | 💰 **${price}** | 🔄 **换乘 ${transfers} 次**\n`;
    output += `\n**详细路线**：\n`;
    
    flat_steps.forEach((step, step_idx) => {
      output += format_transit_step(step, step_idx + 1) + '\n';
    });
    
    output += '\n---\n\n';
  });
  
  // 提示还有更多路线
  if (total > max_show) {
    output += `> 还有 ${total - max_show} 条路线可选，可在同程旅行 APP 中查看更多。\n`;
  }
  
  return output;
}

module.exports = {
  // 共享
  extract_booking_links,
  render_booking_buttons,
  format_duration,
  // 中转 / 联程
  format_transfer_segment,
  format_transfer_info,
  format_transfer_trip,
  // 卡片（按品类）
  format_bus_card,
  format_flight_card,
  format_hotel_card,
  format_scenery_card,
  format_traffic_card,
  format_train_card,
  format_trip_card,
  // 表格（按品类）
  format_bus_table,
  format_flight_table,
  format_flight_table_special,
  format_hotel_table,
  format_scenery_table,
  format_train_table,
  format_trip_table,
  // 补偿交通
  format_supplement_traffic,
  // 度假行程规划块
  format_trip_plan,
  format_trip_plans,
  // 公交地铁
  format_transit_route
};
