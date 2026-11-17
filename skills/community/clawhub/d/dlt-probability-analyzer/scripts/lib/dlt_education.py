# -*- coding: utf-8 -*-
"""
大乐透「彩民防坑 / 玩家教育」模块（描述性 · 非预测）

目标：让系统"更懂彩民"——用大白话讲清四大认知偏差(钱包杀手)、
反骗局警示、近失效应解释。所有内容均基于博彩心理学/行为经济学实证
(Journal of Gambling Studies, NCPG, 中科院数学所, 体彩官方警示)，
不改变任何预测输出，守住一致性红线。

依赖：仅标准库；HTML 片段复用报告既有 CSS 类(.section/.section-title/.info/.warning)。
"""

# 四大认知偏差(钱包杀手) —— 数据来源: Ariyabuddhiphongs & Phengphol 2008 (J Gambling Studies);
# Orford 2005; 体彩官方/央视网反诈提醒。
_BIASES = [
    {
        "icon": "🎲",
        "name": "赌徒谬误 (Gambler's Fallacy)",
        "what": "连买N期没中，就觉得“下一期该轮到我了”；或觉得刚开过的号“短期内不会再开”。",
        "truth": "每期开奖相互独立，球没有记忆。连亏100期，下一期中奖概率仍是精确的 1/21,425,712，不会因“憋久了”而变大。",
        "fix": "把“该中了”换成“概率恒定”。想停就停，别等“回本”。",
    },
    {
        "icon": "🔻",
        "name": "近失效应 (Near-Miss)",
        "what": "上期擦边中到4个号，觉得“就差一点点，下次准中”；这种“差点上”的兴奋感会让人更想追。",
        "truth": "“擦边”在数学上等于零中奖。差1个号和差5个号，奖金都是0；它不会让下一期更近。",
        "fix": "把“差点中”当成“没中”。近失是随机的一部分，不是“信号”。",
    },
    {
        "icon": "🔗",
        "name": "沉没成本 / 套牢 (Entrapment)",
        "what": "“已经投了这么多钱，现在停手前面都白花了”——于是越亏越追，想一次翻本。",
        "truth": "过去的投入已经没了，和下一期开奖毫无关系。追号不会把本捞回来，只会增加总亏损。",
        "fix": "每期独立记账。问自己：“如果今天从未买过，我还会花这笔钱吗？”会，就当娱乐；不会，就停。",
    },
    {
        "icon": "🕹️",
        "name": "控制幻觉 (Illusion of Control)",
        "what": "自选号、研究走势图、守号，让人误以为“我对结果有掌控”，觉得自选比机选更会中。",
        "truth": "机选和自选中奖概率完全相同(都=1/21,425,712)。走势图是开奖后的“事后总结”，挖不出未来规律。",
        "fix": "把选号当“仪式感/乐趣”，别当“策略”。真要省心，机选和自选一样。",
    },
]


def render_education_html():
    """返回「彩民防坑指南」HTML 片段（用于注入报告）。"""
    cards = ""
    for b in _BIASES:
        cards += f"""
        <div style="border:1px solid #2a3358; border-radius:8px; padding:10px 12px; margin:8px 0; background:#10122a;">
          <div style="font-size:14px; font-weight:700; color:#ffd9a0;">{b['icon']} {b['name']}</div>
          <div style="font-size:12px; color:#c7ccea; line-height:1.7; margin:5px 0;">
            <b style="color:#ff9a9a;">陷阱：</b>{b['what']}
          </div>
          <div style="font-size:12px; color:#bfe3c0; line-height:1.7;">
            <b>真相：</b>{b['truth']}
          </div>
          <div style="font-size:12px; color:#9fb4ff; line-height:1.7;">
            <b>怎么破：</b>{b['fix']}
          </div>
        </div>"""

    html = f"""
<div class="section">
<div class="section-title">🧠 彩民防坑指南：你的大脑有 4 个“钱包陷阱”</div>
<div class="info" style="border-color:#5577ff; background:#10122a;">
<p style="color:#aab4ff; font-size:12.5px; line-height:1.8; margin:6px 0;">
下面的内容不改变任何中奖概率（那玩意儿数学上锁死在 1/21,425,712），
但能帮你<b style="color:#ffd9a0;">少亏、不被割、不滑向问题赌博</b>。
这些是博彩心理学反复验证的认知偏差，和你聪不聪明无关——是人脑的通病。
</p>
</div>
{cards}

<div style="border:1px solid #5a2a2a; border-radius:8px; padding:10px 12px; margin:10px 0; background:#1a1014;">
  <div style="font-size:14px; font-weight:700; color:#ff8a8a;">🚨 反骗局警示（官方明令）</div>
  <ul style="font-size:12px; color:#ffc9c9; line-height:1.85; margin:6px 0; padding-left:20px;">
    <li>任何「付费荐号 / 带单群 / 必中计划 / 不中包退」都<b>是骗局</b>（违反《彩票管理条例》，涉嫌诈骗）。</li>
    <li>唯一合法购彩渠道 = <b>线下体彩实体店</b>；凡要求「下载App购彩 / 线上充值 / 陌生转账」均为非法。</li>
    <li>“大师”让不同人买不同号、只晒中奖的——是选择性展示套路，与选号方法无关。</li>
    <li>建议安装「国家反诈中心APP」。遇到要钱预测的，直接拉黑。</li>
  </ul>
</div>

<div style="border:1px solid #2a3358; border-radius:8px; padding:10px 12px; margin:10px 0; background:#10122a;">
  <div style="font-size:13px; font-weight:700; color:#ffd9a0;">🪞 你中了几条？（诚实自检）</div>
  <ul style="font-size:12px; color:#c7ccea; line-height:1.9; margin:6px 0; padding-left:20px;">
    <li>□ 连亏之后，心里冒出过“该轮到我了”</li>
    <li>□ 擦边中奖后，更想接着买“趁热”</li>
    <li>□ 因为“已经花了很多”而舍不得停</li>
    <li>□ 觉得自选/守号比机选“更会中”</li>
    <li>□ 单期花超过 50 元时，没问过自己“是不是上头了”</li>
  </ul>
  <p style="font-size:11.5px; color:#8fa0c8; margin:4px 0 0;">勾中 2 条以上，说明你正被偏差推着走——这不是批评，是提醒你回到“娱乐消费”的定位。</p>
</div>

<p style="font-size:12px; color:#9fb4ff; line-height:1.8; margin:8px 0 0;">
📌 数据锚点：大乐透返奖率≈<b>51%</b>，每注 2 元长期平均拿回约 1.02 元，<b>净期望≈ -0.98 元/注</b>。
买得越多，平均亏得越干净（大数定律）。把购彩当“2 元买个期待+做公益”，才是最稳的赢家心态。
</p>
</div>
"""
    return html


if __name__ == '__main__':
    print(render_education_html())
