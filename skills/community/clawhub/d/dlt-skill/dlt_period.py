# -*- coding: utf-8 -*-
"""
期号计算工具 — 统一所有模块的下期期号逻辑, 避免发散导致 BUG。

大乐透规则:
  - 前区 1-35 选 5, 后区 1-12 选 2
  - 每周一/三/六 21:00 开奖
期号编码: YY + SSS  (SSS = 当年第几期, 从 1 开始)
  - 例: 26084 = 2026 年第 84 期
  - 年末最后一组(约 26156~26158)之后, 下一组进入下一年 → 27001

为何用"日期"而不是固定阈值:
  - 每年实际开奖期数在 150~158 之间浮动(闰年可能多 1~2 期),
    用固定阈值(如 >156 或 >158)在"年份提早结束"时会产生若干虚假期号
    (例如 26156→26157 而非 27001)。
  - 正确做法: 用最新一期开奖日期推算"下一开奖日", 若跨入下一自然年则进年。
    因为开奖固定在周一/三/六, 年末最后一组与元旦最多相隔 3 天, 此推算永远正确。
"""
from datetime import datetime, timedelta

# 周一->周三(+2), 周三->周六(+3), 周六->下周一(+2)
_NEXT_DRAW_DELTA = {0: 2, 2: 3, 5: 2}


def _next_draw_date(d):
    """给定一期开奖日期, 返回下一期开奖日期 (下一个周一/三/六)"""
    return d + timedelta(days=_NEXT_DRAW_DELTA[d.weekday()])


def next_period(latest_period, latest_date=None):
    """计算下一期期号。

    Args:
        latest_period: int 或 str, 如 26084
        latest_date:   str 'YYYY-MM-DD' 或 None
    Returns:
        str, 如 '26085' / '27001'
    """
    yp = int(latest_period) // 1000
    sp = int(latest_period) % 1000 + 1  # 当年序列 +1

    if latest_date:
        try:
            d = datetime.strptime(str(latest_date)[:10], '%Y-%m-%d')
            nd = _next_draw_date(d)
            nyp = nd.year - 2000
            if nyp != yp:
                # 下一开奖日已进入下一年 → 期号进年, 序列归 1
                return f'{nyp}001'
            # 同年: 直接用 sp (已 +1)
        except Exception:
            # 日期解析失败, 退回安全上限 (每年最多约158期)
            if sp > 158:
                yp += 1
                sp = 1
    else:
        # 无日期信息, 退回安全上限
        if sp > 158:
            yp += 1
            sp = 1

    return f'{yp}{sp:03d}'


if __name__ == '__main__':
    # 自检: 覆盖典型与边界场景
    cases = [
        (26084, '2026-07-27', '26085'),  # 当前 (周一/三/六 -> 下一开奖日, 同年)
        (26085, '2026-07-29', '26086'),  # 同年
        (26156, '2026-12-30', '27001'),  # 2026最后一组(周三)->元旦后周六, 进年
        (27001, '2027-01-02', '27002'),  # 新年第二组
        (28158, '2028-12-30', '29001'),  # 闰年最多158期, 年末->进年
    ]
    ok = True
    for p, dt, exp in cases:
        got = next_period(p, dt)
        flag = 'OK ' if got == exp else 'FAIL'
        if got != exp:
            ok = False
        print(f"  [{flag}] {p} ({dt}) -> {got}  期望 {exp}")
    print("  全部通过" if ok else "  *** 存在失败 ***")
