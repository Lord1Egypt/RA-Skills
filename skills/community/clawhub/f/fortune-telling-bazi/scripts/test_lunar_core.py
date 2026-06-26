#!/usr/bin/env python3
import os
import random
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calc import calculate_fate
from lunar_core import Solar


RANDOM_SEED = 20260426
RANDOM_CASE_COUNT = 128
RANDOM_START = date(1901, 1, 1)
RANDOM_END = date(2059, 12, 31)


def random_solar_cases():
    rng = random.Random(RANDOM_SEED)
    start = RANDOM_START.toordinal()
    end = RANDOM_END.toordinal()
    cases = []
    for _ in range(RANDOM_CASE_COUNT):
        day = date.fromordinal(rng.randint(start, end))
        cases.append((
            day.year,
            day.month,
            day.day,
            rng.randrange(24),
            rng.randrange(60),
            rng.randrange(60),
        ))
    return cases


class LunarCoreTest(unittest.TestCase):
    def test_known_bazi_examples(self):
        cases = [
            {
                "args": ("case_1987_spring", 1987, 3, 14, 16, 30, "男"),
                "bazi": "丁卯 癸卯 壬戌 戊申",
                "lunar_str": "1987年2月15日",
                "shengxiao": "兔",
                "mingge": "阳刃格",
                "wangshuai": "弱",
                "xiyong": "水 金",
            },
            {
                "args": ("case_1998_before_new_year", 1998, 1, 19, 16, 0, "女"),
                "bazi": "丁丑 癸丑 丙寅 丙申",
                "lunar_str": "1997年12月21日",
                "shengxiao": "牛",
                "mingge": "正官格",
                "wangshuai": "弱",
                "xiyong": "火 木",
            },
            {
                "args": ("case_2000_before_lichun", 2000, 2, 1, 0, 30, "男"),
                "bazi": "己卯 丁丑 己丑 甲子",
                "lunar_str": "1999年12月26日",
                "shengxiao": "兔",
                "mingge": "偏印格",
                "wangshuai": "弱",
                "xiyong": "土 火",
            },
            {
                "args": ("case_1987_before_lichun", 1987, 1, 30, 0, 0, "女"),
                "bazi": "丙寅 辛丑 己卯 甲子",
                "lunar_str": "1987年1月2日",
                "shengxiao": "兔",
                "mingge": "食神格",
                "wangshuai": "弱",
                "xiyong": "土 火",
            },
            {
                "args": ("case_1987_winter", 1987, 12, 21, 0, 0, "男"),
                "bazi": "丁卯 壬子 甲辰 甲子",
                "lunar_str": "1987年11月1日",
                "shengxiao": "兔",
                "mingge": "偏印格",
                "wangshuai": "强",
                "xiyong": "金 火 土",
            },
            {
                "args": ("case_1969_summer", 1969, 7, 20, 20, 17, "男"),
                "bazi": "己酉 辛未 丙申 戊戌",
                "lunar_str": "1969年6月7日",
                "shengxiao": "鸡",
                "mingge": "正财格",
                "wangshuai": "弱",
                "xiyong": "火 木",
            },
            {
                "args": ("case_1976_autumn", 1976, 9, 9, 9, 9, "女"),
                "bazi": "丙辰 丁酉 甲子 己巳",
                "lunar_str": "1976年8月16日",
                "shengxiao": "龙",
                "mingge": "伤官格",
                "wangshuai": "弱",
                "xiyong": "木 水",
            },
            {
                "args": ("case_1984_start", 1984, 2, 4, 23, 30, "男"),
                "bazi": "甲子 丙寅 戊辰 甲子",
                "lunar_str": "1984年1月3日",
                "shengxiao": "鼠",
                "mingge": "偏印格",
                "wangshuai": "弱",
                "xiyong": "土 火",
            },
            {
                "args": ("case_1990_midday", 1990, 6, 1, 12, 0, "女"),
                "bazi": "庚午 壬午 丁酉 丙午",
                "lunar_str": "1990年5月9日",
                "shengxiao": "马",
                "mingge": "正官格",
                "wangshuai": "强",
                "xiyong": "金 水 土",
            },
            {
                "args": ("case_2012_leap_year", 2012, 2, 29, 6, 45, "男"),
                "bazi": "壬辰 癸卯 庚申 己卯",
                "lunar_str": "2012年2月8日",
                "shengxiao": "龙",
                "mingge": "伤官格",
                "wangshuai": "弱",
                "xiyong": "金 土",
            },
            {
                "args": ("case_2024_new_year", 2024, 2, 10, 8, 0, "女"),
                "bazi": "甲辰 丙寅 甲辰 戊辰",
                "lunar_str": "2024年1月1日",
                "shengxiao": "龙",
                "mingge": "食神格",
                "wangshuai": "强",
                "xiyong": "金 火 土",
            },
            {
                "args": ("case_2059_late", 2059, 12, 31, 22, 59, "男"),
                "bazi": "己卯 丙子 壬申 辛亥",
                "lunar_str": "2059年11月27日",
                "shengxiao": "兔",
                "mingge": "偏财格",
                "wangshuai": "强",
                "xiyong": "木 火 土",
            },
        ]

        self.assertGreaterEqual(len(cases), 10)

        for case in cases:
            with self.subTest(name=case["args"][0]):
                fate = calculate_fate(*case["args"])
                got_bazi = " ".join(fate["bazi"].values())
                self.assertEqual(got_bazi, case["bazi"])
                for field in ("lunar_str", "shengxiao", "mingge", "wangshuai", "xiyong"):
                    self.assertEqual(fate[field], case[field])

    def test_random_solar_lunar_round_trip(self):
        cases = random_solar_cases()
        self.assertGreaterEqual(len(cases), 100)

        for args in cases:
            with self.subTest(args=args):
                solar = Solar.fromYmdHms(*args)
                round_trip = solar.getLunar().getSolar()
                self.assertEqual(
                    (
                        round_trip.getYear(),
                        round_trip.getMonth(),
                        round_trip.getDay(),
                        round_trip.getHour(),
                        round_trip.getMinute(),
                        round_trip.getSecond(),
                    ),
                    args,
                )


if __name__ == "__main__":
    unittest.main()
