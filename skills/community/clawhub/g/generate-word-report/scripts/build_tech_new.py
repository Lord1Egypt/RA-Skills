def build_tech(mdata):
    """第四章：科技方面——只保留巨头并购、资本运作、境外IPO等核心事件"""
    import re

    def full_kw(text, kws):
        for kw in kws:
            if kw in text:
                return True
        return False

    # 核心事件词
    CORE_KWS = [
        '并购', '收购', '合并', '要约收购', '私有化',
        '上市', 'IPO', '境外上市', '港股上市', '美股上市', '纳斯达克',
        '回购', '配股', '减持', '增持', '定向增发',
        '拆分', '分拆', '募资',
    ]
    # 排除词（完整匹配）
    SKIP_EXACT = [
        '新能源', '汽车', '小订', '投资者',
    ]

    def clean_event(text):
        if not text:
            return ''
        text = re.sub(r'\(文章[。.][^)]*\)', '', text)
        text = re.sub(r'\d{4}[-/]\d{2}[-/]\d{2}\s*[·\-–—]\S.*$', '', text)
        text = re.sub(r'[·\-]\S{2,}(?:官方)?(?:网易号|搜狐号|百家号)?$', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def is_core_event(item):
        event = item.get('事件', '')
        company = item.get('公司', '')
        if full_kw(company, SKIP_EXACT):
            return False
        if full_kw(event, SKIP_EXACT):
            return False
        combined = event + company
        if not full_kw(combined, CORE_KWS):
            return False
        # 上市 without capital op keywords -> exclude
        if full_kw(event, ['上市']) and not full_kw(event, ['并购', '收购', 'IPO', '增发', '配股', '回购', '募资']):
            return False
        # 融资 without details -> exclude
        if full_kw(combined, ['融资', '募资']):
            concrete = any(kw in event for kw in ['亿美元', '万美元', '亿元人民币', '收购', '并购', 'IPO', '上市', '增发', '配股', '回购', '募资'])
            if not concrete:
                return False
        return True

    def make_key(item):
        company = item.get('公司', '').strip()
        event = clean_event(item.get('事件', ''))
        return (company + '|' + event)[:50]

    tech = mdata.get('科技企业动态', {})
    all_items = []
    for region_items in tech.values():
        if isinstance(region_items, list):
            all_items.extend(region_items)

    # Filter to core events
    filtered = [item for item in all_items if is_core_event(item)]

    # Deduplicate
    seen = set()
    deduped = []
    for item in filtered:
        key = make_key(item)
        if key not in seen:
            seen.add(key)
            deduped.append(item)

    # Build paragraphs (max 3)
    paragraphs = []
    for item in deduped[:3]:
        event = clean_event(item.get('事件', ''))
        company = item.get('公司', '').strip()
        if not event:
            continue
        if company and len(company) > 4 and not event.startswith(company[:5]):
            text = company + '：' + event
        else:
            text = event
        paragraphs.append(text)

    return paragraphs if paragraphs else ['暂无科技企业重大动态。']
