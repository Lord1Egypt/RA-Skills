import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from content_gate import (check, cn_numerals_to_arabic, content_features,  # noqa: E402
                          count_first_person, fact_numbers, find_absolute_words,
                          hook_overlap, missing_category_info, resolve_category)

FACTS = {"shop": "莫摧咖啡（三圣乡店）", "per_capita": 38,
         "notes": ["等位十五分钟", "两个人", "脏脏拿铁 32 元"]}
REVIEW_BODY = (
    "周末下午我们两个人临时起意过来，等位 15 分钟。我点了脏脏拿铁 32 元，"
    "奶味重但不腻，杯子摸着是温的不是烫的。人均 38，座位不多，"
    "靠窗那排能看到外面的花田，坐久了也没人催。我觉得适合下午来坐一会儿，"
    "饭点前后人会多一些。店里音乐声音不大，聊天不费劲，桌子间距也够宽。"
    "你们去三圣乡一般喝咖啡还是喝茶？"
)


def get(report, name_prefix):
    return next(r for r in report["results"] if r["check"].startswith(name_prefix))


class AbsoluteWordsTest(unittest.TestCase):
    def test_everyday_phrases_exempt(self):
        self.assertEqual(find_absolute_words("第一次来，第一口就喜欢，最好提前预约"), [])

    def test_real_absolute_words_hit(self):
        self.assertIn("最好", find_absolute_words("这是我喝过最好的拿铁"))
        self.assertIn("第一", find_absolute_words("成都第一"))
        self.assertIn("最好吃", find_absolute_words("最好吃的烧鹅"))


class FactsTest(unittest.TestCase):
    def test_cn_numerals(self):
        self.assertEqual(cn_numerals_to_arabic("两个人等了十五分钟"), "2个人等了15分钟")
        self.assertEqual(cn_numerals_to_arabic("二十"), "20")

    def test_fact_numbers(self):
        self.assertLessEqual({38.0, 15.0, 2.0, 32.0}, fact_numbers(FACTS))

    def test_orphan_number_blocks(self):
        report = check("", REVIEW_BODY + "排队 40 分钟。", "review", FACTS)
        self.assertFalse(report["pass"])
        self.assertIn("40", get(report, "数字有出处")["detail"])

    def test_all_numbers_sourced_pass(self):
        report = check("", REVIEW_BODY, "review", FACTS)
        self.assertTrue(report["pass"], report)

    def test_missing_facts_is_warning_only(self):
        report = check("", REVIEW_BODY, "review", None)
        self.assertTrue(report["pass"])
        self.assertEqual(get(report, "数字有出处")["level"], "warn")


class KindRulesTest(unittest.TestCase):
    def test_review_does_not_need_title(self):
        self.assertTrue(check("", REVIEW_BODY, "review", FACTS)["pass"])

    def test_note_requires_title(self):
        report = check("", REVIEW_BODY * 2, "note", FACTS)
        self.assertFalse(get(report, "标题")["pass"])

    def test_exclamation_is_warning(self):
        report = check("", REVIEW_BODY + "好喝！！", "review", FACTS)
        self.assertTrue(report["pass"])
        self.assertTrue(any(w["check"].startswith("感叹号") for w in report["warnings"]))


class PlaybookChecksTest(unittest.TestCase):
    def test_per_capita_mismatch_blocks(self):
        facts = {**FACTS, "notes": FACTS["notes"] + ["人均 50-60"]}
        body = REVIEW_BODY.replace("人均 38", "人均 50-60")
        self.assertFalse(get(check("", body, "review", facts), "人均一致")["pass"])
        self.assertTrue(get(check("", body, "review", facts, per_capita=55), "人均一致")["pass"])

    def test_per_capita_from_facts(self):
        self.assertTrue(get(check("", REVIEW_BODY, "review", FACTS), "人均一致")["pass"])

    def test_ending_question_warns(self):
        self.assertTrue(get(check("", REVIEW_BODY, "review", FACTS), "结尾提问")["pass"])
        body = REVIEW_BODY.replace("你们去三圣乡一般喝咖啡还是喝茶？", "下次还来。")
        report = check("", body, "review", FACTS)
        self.assertTrue(report["pass"])
        self.assertFalse(get(report, "结尾提问")["pass"])

    def test_hook_overlap_real_case(self):
        siblings = [{"type": "review", "hook": "58元一小时，带娃在公园骑了11公里"}]
        self.assertIsNotNone(hook_overlap("天府公园亲子骑行攻略：58元骑了11公里", siblings[0]["hook"]))
        self.assertIsNotNone(hook_overlap("成都这家院子咖啡，把荷塘变成了大堂", "荷塘边喝咖啡的院子，成都少见"))
        self.assertIsNone(hook_overlap("天府公园骑行路线：秦皇湖段下午四点后顺光", siblings[0]["hook"]))
        report = check("天府公园亲子骑行攻略：58元骑了11公里", REVIEW_BODY * 2, "note", None, siblings=siblings)
        self.assertFalse(get(report, "开头卖点")["pass"])

    def test_features(self):
        f = content_features("天府公园亲子骑行攻略：58元骑了11公里", REVIEW_BODY, [])
        self.assertTrue(f["title_has_number"])
        self.assertEqual(f["title_audience"], ["亲子"])
        self.assertTrue(f["ends_with_question"])
        self.assertIsNone(content_features("", REVIEW_BODY)["title_has_number"])


class CategoryRulesTest(unittest.TestCase):
    def test_resolve(self):
        self.assertEqual(resolve_category("休闲娱乐·陶艺体验"), "亲子体验")
        self.assertEqual(resolve_category("餐饮"), "餐饮")
        self.assertEqual(resolve_category("咖啡"), "餐饮")
        self.assertIsNone(resolve_category(""))
        self.assertIsNone(resolve_category("宠物医院"))

    def test_missing_items_warn_only(self):
        facts = {**FACTS, "category": "亲子体验"}
        report = check("", REVIEW_BODY, "review", facts)
        self.assertTrue(report["pass"])
        r = get(report, "品类必写")
        self.assertFalse(r["pass"])
        self.assertIn("交通或停车", r["detail"])

    def test_real_tongzhi_review_covers_all(self):
        body = ("我们这次带娃来同治龙窑，参观是免费的，制作陶罐2个100元，老师可以在旁边指导。"
                "上午拉坯，离市区30多公里，适合自驾；吃饭可以去周边1公里的镇上。适合亲子家庭。")
        self.assertEqual(missing_category_info(body, "亲子体验"), [])


class ConversionAndStyleTest(unittest.TestCase):
    def test_hard_sell_blocks(self):
        report = check("", REVIEW_BODY + "错过后悔，赶紧冲。", "review", FACTS)
        self.assertFalse(get(report, "硬推销")["pass"])
        self.assertFalse(report["pass"])

    def test_merchant_voice_blocks(self):
        report = check("", REVIEW_BODY + "本店限时优惠。", "review", FACTS)
        self.assertFalse(get(report, "商家口吻")["pass"])

    def test_ai_cliche_blocks(self):
        report = check("", "值得一提的是，" + REVIEW_BODY, "review", FACTS)
        self.assertFalse(get(report, "AI腔套话")["pass"])
        body = REVIEW_BODY + "这不仅是一杯咖啡，更是一种生活态度。"
        self.assertFalse(get(check("", body, "review", FACTS), "AI腔套话")["pass"])

    def test_action_and_not_for_warn_only(self):
        report = check("", REVIEW_BODY, "review", FACTS)
        self.assertTrue(report["pass"])
        self.assertTrue(get(report, "行动信息")["pass"])
        self.assertFalse(get(report, "写了不适合谁")["pass"])
        body = REVIEW_BODY.replace("饭点前后人会多一些。", "饭点前后人会多一些，想安静聊天的不太适合。")
        self.assertTrue(get(check("", body, "review", FACTS), "写了不适合谁")["pass"])

    def test_dash_parallel_uniform_warn(self):
        body = REVIEW_BODY + "环境——很好——安静。"
        self.assertFalse(get(check("", body, "review", FACTS), "破折号")["pass"])
        par = "我喜欢它的拿铁，我喜欢它的座位，我喜欢它的音乐。" + REVIEW_BODY
        report = check("", par, "review", FACTS)
        self.assertTrue(report["pass"])
        self.assertFalse(get(report, "无排比三连")["pass"])
        flat = "这家咖啡店很安静。拿铁味道还不错。座位离窗户很近。店员说话很客气。我们坐了挺久的。"
        self.assertFalse(get(check("", flat, "review", FACTS), "长短句交错")["pass"])
        self.assertTrue(get(check("", REVIEW_BODY, "review", FACTS), "长短句交错")["pass"])


class MiscTest(unittest.TestCase):
    def test_first_person_not_double_counted(self):
        self.assertEqual(count_first_person("我们来了，我点了"), 2)

    def test_diversion(self):
        report = check("", REVIEW_BODY + "加微信 abc 领券", "review", FACTS)
        self.assertFalse(get(report, "站外导流")["pass"])
        report = check("", REVIEW_BODY + "电话 13812345678", "review", FACTS)
        self.assertFalse(get(report, "站外导流")["pass"])

    def test_vx_shorthand_needs_context(self):
        # 光秃秃的 VX 不拦（密室主题名、品牌名里会出现）
        report = check("", REVIEW_BODY + "玩的是 VX 主题，机关不少", "review", FACTS)
        self.assertTrue(get(report, "站外导流")["pass"])
        # 有联系意图的三种语境才拦
        for ctx in ("加VX abc123", "VX号 abc123", "VX: abc123"):
            report = check("", REVIEW_BODY + ctx, "review", FACTS)
            self.assertFalse(get(report, "站外导流")["pass"], ctx)


if __name__ == "__main__":
    unittest.main()
