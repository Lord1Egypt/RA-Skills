# 本文件统一定义“同一条内容”的判定规则，以及多个来源版本的优先级规则。

IMPORTANT_SOURCE_TYPES = {"newsflash_important", "article_important"}


def canonical_content_key(item):
    """同一条内容优先按 URL 归一化；无 URL 时退回标题+发布时间。"""
    url = (item.get("url") or "").strip()
    if url:
        return url
    title = (item.get("title") or "").strip()
    published_at = (item.get("published_at") or "").strip()
    return "%s|%s" % (title, published_at)


def source_priority(item):
    """important 版本优先，其次发布时间更新的优先。"""
    return (
        item.get("source_type") in IMPORTANT_SOURCE_TYPES,
        item.get("published_at") or "",
    )


def pick_representative_record(records):
    """在多个来源版本中选出最适合用于展示和统计的代表记录。"""
    chosen = None
    for record in records:
        if chosen is None or source_priority(record) > source_priority(chosen):
            chosen = record
    return chosen
