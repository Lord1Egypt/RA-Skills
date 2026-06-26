def fetch_us_employment():
    """美国就业市场专项数据 - 优化增强版
    采集：当周初请、续请、四周均值、Challenger裁员、非农前瞻
    数据源：FRED（初请/续请/均值）+ Web Search（Challenger/非农前瞻）
    严格区分：当期值、预期值、前值（修正前后）
    """
    import requests, re, time, random
    import logging
    log = logging.getLogger('collector')

    employment = {}

    # ─── FRED 封装 ───────────────────────────────────────────
    def _fred(sid, limit=15):
        """从FRED CSV拉数据，返回[(date, val), ...]"""
        for attempt in range(3):
            try:
                time.sleep(random.uniform(1.0, 2.5))
                url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&limit={limit}'
                r = requests.get(url, timeout=15)
                if r.status_code != 200:
                    continue
                lines = r.text.strip().split('\n')
                data = []
                for line in lines[1:]:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        date = parts[0].strip()
                        raw = parts[-1].strip()
                        if raw not in ('.', 'N/A', '', 'nan', 'None') and raw.replace('.', '').replace('-', '').isdigit():
                            try:
                                val = float(raw)
                                data.append((date, val))
                            except:
                                pass
                return data
            except Exception as e:
                log.warning(f'  [FRED] {sid} 异常: {e}')
                time.sleep(random.uniform(2, 4))
        return []

    def _fred_latest(sid, limit=15):
        """返回 (当期date, 当期val, 前值date, 前值val)"""
        data = _fred(sid, limit)
        if not data or len(data) < 2:
            return None, None, None, None
        # data: oldest→newest
        latest_date, latest_val = data[-1]
        prev_date, prev_val = data[-2]
        return latest_date, latest_val, prev_date, prev_val

    # ─── Web Search 封装 ─────────────────────────────────────
    def _ws(query, max_results=5):
        """Web Search，回退逻辑"""
        try:
            results = ws_fallback.search(query, max_results=max_results)
            return ' '.join([r.get('content', '') or r.get('snippet', '') for r in results])
        except Exception as e:
            log.warning(f'  [WS] search failed: {e}')
            return ''

    # ══════════════════════════════════════════════════════════
    # 指标1：当周初请失业金人数 (ICSA)
    # FRED序列：ICSA = Initial Claims Seasonally Adjusted
    # ══════════════════════════════════════════════════════════
    date_cur, val_cur, date_prev, val_prev = _fred_latest('ICSA', limit=15)
    if val_cur is not None:
        employment['当周初请失业金'] = {
            '当期值': round(val_cur),
            '前值': round(val_prev) if val_prev is not None else '暂未披露',
            '前值期间': date_prev,
            '单位': '万人',
            '期间': date_cur,
            'source': 'FRED(ICSA)',
            '备注': 'seasonally adjusted',
        }
        log.info(f'  ✅ 当周初请: {round(val_cur)}万 ({date_cur}), 前值: {round(val_prev) if val_prev else "N/A"}万 ({date_prev})')
    else:
        employment['当周初请失业金'] = {
            '当期值': '暂未披露',
            '前值': '暂未披露',
            '单位': '万人',
            'source': 'FRED',
        }
        log.warning('  ⚠️ 当周初请: 数据获取失败')

    # ══════════════════════════════════════════════════════════
    # 指标2：初请四周均值 (IC4WSA)
    # FRED序列：IC4WSA = 4-week moving average of initial claims
    # 计算边际变化：当期均值 vs 上期均值
    # ══════════════════════════════════════════════════════════
    date_ic4, val_ic4, date_ic4_prev, val_ic4_prev = _fred_latest('IC4WSA', limit=15)
    if val_ic4 is not None:
        change = None
        if val_ic4_prev is not None:
            change = round(val_ic4 - val_ic4_prev)
        employment['初请四周均值'] = {
            '当期值': round(val_ic4),
            '前值': round(val_ic4_prev) if val_ic4_prev is not None else '暂未披露',
            '前值期间': date_ic4_prev,
            '边际变化': f'+{change}' if change and change > 0 else str(change) if change else '暂未披露',
            '单位': '万人',
            '期间': date_ic4,
            'source': 'FRED(IC4WSA)',
            '备注': '四周均值不含当周单周数据',
        }
        log.info(f'  ✅ 初请四周均值: {round(val_ic4)}万 ({date_ic4}), 前值: {round(val_ic4_prev) if val_ic4_prev else "N/A"}万, 边际: {change}')
    else:
        employment['初请四周均值'] = {
            '当期值': '暂未披露',
            '前值': '暂未披露',
            '边际变化': '暂未披露',
            '单位': '万人',
            'source': 'FRED(IC4WSA)',
        }
        log.warning('  ⚠️ 初请四周均值: 数据获取失败')

    # ══════════════════════════════════════════════════════════
    # 指标3：续请失业金人数 (CCSA)
    # FRED序列：CCSA = Continued Claims Seasonally Adjusted
    # ══════════════════════════════════════════════════════════
    date_ccsa, val_ccsa, date_ccsa_prev, val_ccsa_prev = _fred_latest('CCSA', limit=15)
    if val_ccsa is not None:
        employment['续请失业金'] = {
            '当期值': round(val_ccsa),
            '前值': round(val_ccsa_prev) if val_ccsa_prev is not None else '暂未披露',
            '前值期间': date_ccsa_prev,
            '单位': '万人',
            '期间': date_ccsa,
            'source': 'FRED(CCSA)',
            '备注': 'seasonally adjusted',
        }
        log.info(f'  ✅ 续请失业金: {round(val_ccsa)}万 ({date_ccsa}), 前值: {round(val_ccsa_prev) if val_ccsa_prev else "N/A"}万')
    else:
        employment['续请失业金'] = {
            '当期值': '暂未披露',
            '前值': '暂未披露',
            '单位': '万人',
            'source': 'FRED(CCSA)',
        }
        log.warning('  ⚠️ 续请失业金: 数据获取失败')

    # ══════════════════════════════════════════════════════════
    # 指标4：Challenger企业裁员人数 + 分项诱因
    # 数据源：Web Search（三引擎轮搜）
    # 字段：公布值、前值、裁员核心诱因及分项占比
    # 重点：AI替代、企业重组、行业拖累等核心因素
    # ══════════════════════════════════════════════════════════
    challenger_q = _ws('Challenger job cuts monthly report current month', max_results=8)
    if challenger_q:
        # 提取裁员总人数
        # Pattern: "X,YZZ" or "X.XX万" or "X,XXX,XXX" style numbers
        raw_patterns = [
            r'(\d{1,3}\,\d{3}\,\d{3})\s*(?:人|人裁员|layoff)',
            r'(\d{1,3}\,\d{3})\s*(?:万)?\s*(?:人|裁员|layoff)',
            r'(\d+\.?\d*)\s*(?:万)?\s*(?:layoff|job\s*cuts|裁员)',
            r'裁员\s*(\d+\.?\d*)\s*(?:万)?\s*(?:人)',
            r'(\d+\.?\d*)\s*(?:万)\s*(?:人)',
        ]
        val_ch = None
        for pat in raw_patterns:
            m = re.search(pat, challenger_q)
            if m:
                raw = m.group(1).replace(',', '')
                try:
                    v = float(raw)
                    # 判断单位：>10000视为人，转万人；<1000视为万
                    if v > 100000:
                        v = v / 10000
                    val_ch = round(v, 2)
                    break
                except:
                    pass

        # 提取前值
        prev_patterns = [
            r'(?:上月|前月|上月为|上月为)\s*(\d+\.?\d*)\s*(?:万)?',
            r'(?:前值|上期)[:\s]*(\d+\.?\d*)\s*(?:万)?',
            r'(\d+\.?\d*)\s*(?:万)\s*(?:人)?.{0,10}?(?:上月|前月)',
        ]
        val_ch_prev = None
        for pat in prev_patterns:
            m = re.search(pat, challenger_q)
            if m:
                try:
                    raw = m.group(1).replace(',', '')
                    v = float(raw)
                    if v > 10000:
                        v = v / 10000
                    val_ch_prev = round(v, 2)
                    break
                except:
                    pass

        # 提取AI替代、企业重组等行业分类占比
        reasons = {}
        reason_patterns = {
            'AI替代/自动化': [r'AI(?:替代|取代|自动化|机器)', r'(?:artificial|AI)\s*(?:replacement|automation)', r'自动化.{0,8}替代', r'机器.{0,8}替代'],
            '企业重组': [r'企业\s*重组', r'公司\s*重组', r'restructur', r'cost\s*cut', r'降本'],
            '行业拖累/需求疲软': [r'行业\s*拖累', r'需求\s*疲软', r'market\s*(?:weak|soft|demand)', r'行业.{0,6}下滑', r'demand.{0,8}(?:soft|weak)'],
            '关税/贸易摩擦': [r'关税', r'tariff', r'贸易.{0,6}摩擦', r'trade\s*war'],
        }
        for reason_name, patterns in reason_patterns.items():
            for pat in patterns:
                if re.search(pat, challenger_q, re.IGNORECASE):
                    reasons[reason_name] = '提及'
                    break

        if val_ch is not None:
            entry = {
                '当期值': val_ch,
                '前值': val_ch_prev if val_ch_prev else '暂未披露',
                '单位': '万人',
                'source': 'Web Search(Challenger)',
            }
            if reasons:
                entry['核心诱因'] = reasons
            employment['Challenger裁员'] = entry
            log.info(f'  ✅ Challenger裁员: {val_ch}万, 前值: {val_ch_prev}, 诱因: {list(reasons.keys()) if reasons else "未明确"}')
        else:
            log.warning('  ⚠️ Challenger裁员: 未解析到有效数据')
    else:
        log.warning('  ⚠️ Challenger裁员: Web Search 无结果')

    # ══════════════════════════════════════════════════════════
    # 指标5：最新非农就业前瞻预测
    # 数据源：Web Search（三引擎）
    # 字段：市场普遍新增就业预期区间、失业率预期数值
    # ══════════════════════════════════════════════════════════
    # 自动判断当前月份（距上次非农发布后的第几周）
    import datetime
    today = datetime.date.today()
    # 每月第一个周五发布非农数据，估算当前所处月份
    # 非农发布后一周内为"当月已发布"，之后为"下月预测"
    # 简单策略：搜"非农就业预测 YYYY年MM月" 或 "NFP forecast month"
    month_names = ['January','February','March','April','May','June',
                   'July','August','September','October','November','December']
    cur_month_name = month_names[today.month - 1]
    prev_month_name = month_names[(today.month - 2) % 12]
    # 尝试两个版本：上月实际 vs 本月预测
    nfp_q = _ws(f'NFP nonfarm payroll forecast {cur_month_name} {today.year} analyst estimate', max_results=8)
    if not nfp_q or len(nfp_q) < 50:
        nfp_q2 = _ws(f'美国非农就业预测 {today.year}年{today.month}月 市场预期', max_results=8)
        nfp_q = nfp_q + ' ' + nfp_q2

    if nfp_q:
        payroll_vals = []
        ur_vals = []

        # 提取新增就业人数（多种模式）
        payroll_patterns = [
            r'(?:新增|预计|预期|估计)\s*(\d+\.?\d*)\s*(?:万)?\s*(?:人|jobs?)',
            r'(\d+\.?\d*)\s*万\s*(?:新增)?\s*(?:就业)?',
            r'(?:新增|increase)\s*(?:of\s*)?(\d+\.?\d*)\s*(?:万)?\s*(?:jobs?|人)',
            r'payroll[s]?\s*(?:estimate|forecast|预期)?[:\s]*(\d+\.?\d*)',
            r'average\s*estimate[:\s]*(\d+\.?\d*)\s*(?:万)?',
        ]
        for pat in payroll_patterns:
            for m in re.finditer(pat, nfp_q):
                raw = m.group(1).replace(',', '')
                try:
                    v = float(raw)
                    if 0 < v < 1000:  # 万人
                        payroll_vals.append(v)
                    elif 1000 <= v <= 5000:
                        payroll_vals.append(v / 10000)
                except:
                    pass

        # 提取失业率
        ur_patterns = [
            r'失业率\s*(\d+\.?\d*)\s*%',
            r'unemployment\s*(?:rate)?\s*(?:预期)?[:\s]*(\d+\.?\d*)\s*%',
            r'(\d+\.?\d*)\s*%\s*(?:失业率|unemployment)',
        ]
        for pat in ur_patterns:
            for m in re.finditer(pat, nfp_q):
                try:
                    v = float(m.group(1))
                    if 0 < v < 20:
                        ur_vals.append(v)
                except:
                    pass

        # 合并去重（同值±0.5取平均）
        def cluster(vals, tol=0.5):
            if not vals:
                return []
            vals = sorted(set(vals))
            clusters = []
            cur = [vals[0]]
            for x in vals[1:]:
                if abs(x - cur[-1]) <= tol:
                    cur.append(x)
                else:
                    clusters.append(sum(cur) / len(cur))
                    cur = [x]
            clusters.append(sum(cur) / len(cur))
            return [round(v, 1) for v in clusters]

        payroll_ests = cluster(payroll_vals, 3.0)
        ur_ests = cluster(ur_vals, 0.2)

        nfp_entry = {
            'source': 'Web Search(NFP前瞻)',
        }
        if payroll_ests:
            if len(payroll_ests) == 1:
                nfp_entry['新增就业预期'] = payroll_ests[0]
            else:
                nfp_entry['新增就业预期区间'] = f'{min(payroll_ests):.0f}~{max(payroll_ests):.0f}'
                nfp_entry['新增就业预期'] = round(sum(payroll_ests) / len(payroll_ests), 1)
            nfp_entry['单位'] = '万人'
        if ur_ests:
            if len(ur_ests) == 1:
                nfp_entry['失业率预期'] = ur_ests[0]
            else:
                nfp_entry['失业率预期区间'] = f'{min(ur_ests):.1f}~{max(ur_ests):.1f}'
                nfp_entry['失业率预期'] = round(sum(ur_ests) / len(ur_ests), 2)
            nfp_entry['失业率单位'] = '%'
        nfp_entry['期间'] = f'{today.year}年{today.month}月'

        employment['非农前瞻预测'] = nfp_entry
        log.info(f'  ✅ 非农前瞻: 新增={nfp_entry.get("新增就业预期","N/A")}万 失业率={nfp_entry.get("失业率预期","N/A")}% 区间={nfp_entry.get("新增就业预期区间","N/A")}')
    else:
        employment['非农前瞻预测'] = {
            '新增就业预期': '暂未披露',
            '失业率预期': '暂未披露',
            'source': 'Web Search(NFP前瞻)',
        }
        log.warning('  ⚠️ 非农前瞻: Web Search 无结果')

    market_data['美国就业市场'] = employment
    log.info(f'  📊 美国就业市场采集完成: {list(employment.keys())}')