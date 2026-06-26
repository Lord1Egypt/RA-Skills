from context_stabilizer import LongTextContextStabilizer, ContextConfig
from context_stabilizer.config import ConsistencyConfig, HistoryConfig

print("=" * 60)
print("长文本上下文稳定器 - 完整功能演示")
print("=" * 60)

custom_config = ContextConfig(
    consistency=ConsistencyConfig(threshold=0.65),
    history=HistoryConfig(max_history=50, auto_save=False)
)

stabilizer = LongTextContextStabilizer()

novel_text = """
第一章 初入江湖
李逍遥，18岁，性格洒脱，嫉恶如仇，手持一把生锈的铁剑，从小在余杭镇长大。
这天，他离开家乡，准备前往苏州城，寻找失散多年的婶婶。

第二章 偶遇灵儿
在去苏州的路上，李逍遥遇到了一位名叫赵灵儿的少女，她温柔善良，身负女娲族的血脉，正被拜月教追杀。
李逍遥出手相救，两人结伴同行。途中，李逍遥得知赵灵儿正在寻找解救族人的方法。
"""

print("\n【1. 初始化文本（自动提取锚点）】")
stabilizer.init_long_text(novel_text, auto_extract=True)

print("自动提取的锚点：")
for key, value in stabilizer.anchor_manager.anchors.items():
    print(f"  {key}: {value}")

print("\n【2. 生成增强提示词】")
user_prompt = "续写第三章，李逍遥和赵灵儿在破庙休息时遭遇拜月教小喽啰袭击"
enhanced_prompt = stabilizer.get_enhanced_prompt(user_prompt)

print("=== 复制以下内容到LLM对话框 ===")
print(enhanced_prompt[:500] + "..." if len(enhanced_prompt) > 500 else enhanced_prompt)

print("\n【3. 模拟LLM生成内容】")
qwen_output = """
第三章 破庙惊魂

夜色如墨，破庙残垣断壁间，篝火摇曳。李逍遥靠在佛像旁，手中铁剑横于膝上，目光警惕地扫视着门外。

"灵儿姑娘，你先休息，我来守夜。"李逍遥洒脱地笑道，眼中却闪过一丝坚毅。

赵灵儿轻轻点头，温柔地说道："李大哥，你也累了一天了，我也能帮忙守夜的。"

话音未落，门外突然传来一阵阴冷的笑声。

"哈哈哈，终于找到你们了！拜月教主有令，捉拿女娲后人！"

三道黑影从门窗跃入，手持弯刀，杀气腾腾。李逍遥瞬间起身，铁剑出鞘，挡在赵灵儿身前。

"想动她？先问问我手中的剑！"

李逍遥嫉恶如仇的性格此刻展露无遗，铁剑挥舞间，与三名刺客战作一团...
"""

print("\n【4. 一致性检查（详细模式）】")
detailed_result = stabilizer.check_consistency(qwen_output, detailed=True)

print(f"总体一致性: {'✓ 通过' if detailed_result['summary']['overall_consistent'] else '✗ 不通过'}")
print(f"发现问题数: {detailed_result['summary']['total_issues']}")
print("\n各维度评分:")
for dim, score in detailed_result['summary']['dimension_scores'].items():
    print(f"  {dim}: {score:.2f}")

if detailed_result['recommendations']:
    print("\n改进建议:")
    for rec in detailed_result['recommendations']:
        print(f"  - {rec}")

print("\n【5. 记录生成历史】")
stabilizer.record_generation(
    user_prompt=user_prompt,
    enhanced_prompt=enhanced_prompt,
    generated_text=qwen_output,
    consistency_check=detailed_result
)
print("已记录本轮生成")

print("\n【6. 标记重要片段】")
stabilizer.mark_important_segment(
    content="李逍遥嫉恶如仇的性格此刻展露无遗",
    reason="角色性格关键描写",
    importance=2.0
)
stabilizer.add_plot_event(
    event="破庙遭遇拜月教袭击",
    characters=["李逍遥", "赵灵儿"],
    importance=2
)
print("已标记重要片段和剧情事件")

print("\n【7. 查看角色和剧情摘要】")
print(f"角色摘要:\n{stabilizer.get_character_summary('李逍遥')}")
print(f"\n剧情摘要:\n{stabilizer.get_plot_summary()}")

print("\n【8. 查看系统统计】")
stats = stabilizer.get_statistics()
print(f"历史记录: {stats['history']['total_turns']} 轮")
print(f"上下文窗口: {stats['window']['total_windows']} 个")
print(f"缓存命中率: {stats['cache']['embedding_cache']['hit_rate']}")

print("\n【9. 检查重复内容】")
repetition_check = stabilizer.check_repetition(qwen_output)
print(f"是否存在重复: {'是' if repetition_check['is_repetitive'] else '否'}")

print("\n" + "=" * 60)
print("演示完成！")
print("=" * 60)

print("\n【高级用法示例】")

print("\n# 自定义配置")
print("""
custom_config = ContextConfig(
    consistency=ConsistencyConfig(threshold=0.75),
    window=WindowConfig(max_window_size=6000),
    history=HistoryConfig(max_history=200, auto_save=True)
)
stabilizer = LongTextContextStabilizer(custom_config)
""")

print("\n# 手动设置锚点")
print("""
manual_anchors = {
    "人设": "李逍遥：18岁，洒脱，嫉恶如仇；赵灵儿：温柔善良，女娲族血脉",
    "世界观": "古风武侠仙侠世界",
    "核心剧情": "李逍遥寻找婶婶，偶遇赵灵儿，结伴同行"
}
stabilizer.init_long_text(text, manual_anchors=manual_anchors, auto_extract=False)
""")

print("\n# 保存和加载会话")
print("""
stabilizer.save_session("my_novel_session")
stabilizer.load_session("my_novel_session")
""")

print("\n# 导出完整故事")
print("""
stabilizer.export_story("output/story.txt", format="txt")
stabilizer.export_story("output/story.json", format="json")
""")
