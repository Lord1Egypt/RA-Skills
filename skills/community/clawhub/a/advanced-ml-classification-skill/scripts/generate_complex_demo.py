#!/usr/bin/env python3
"""生成复杂多分类演示数据。"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path


def generate(path: Path, n_rows: int = 2500, seed: int = 20260304) -> None:
    random.seed(seed)

    cities = ["Shanghai", "Beijing", "Shenzhen", "Guangzhou", "Hangzhou", "Chengdu"]
    departments = ["Sales", "Product", "Tech", "Support", "Finance", "HR"]
    edu_levels = ["高中", "本科", "硕士", "博士"]
    channels = ["Online", "Referral", "Event", "Partner", "Ad"]

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "age",
                "income",
                "city",
                "department",
                "education",
                "years_experience",
                "projects_last_year",
                "avg_weekly_hours",
                "overtime_hours",
                "cert_count",
                "remote_ratio",
                "satisfaction",
                "manager_score",
                "late_days",
                "customer_tickets",
                "acquisition_channel",
                "target_label",
            ]
        )

        for _ in range(n_rows):
            age = random.randint(21, 58)
            city = random.choice(cities)
            department = random.choice(departments)
            education = random.choices(edu_levels, weights=[0.12, 0.58, 0.25, 0.05], k=1)[0]
            years_experience = max(0, int(random.gauss(7, 4)))
            projects_last_year = max(1, int(random.gauss(6, 2.5)))
            avg_weekly_hours = max(30, int(random.gauss(47, 7)))
            overtime_hours = max(0, int(random.gauss(6, 4)))
            cert_count = max(0, int(random.gauss(2.2, 1.8)))
            remote_ratio = random.choice([0, 20, 40, 60, 80, 100])
            satisfaction = round(min(5.0, max(1.0, random.gauss(3.4, 0.8))), 2)
            manager_score = round(min(5.0, max(1.0, random.gauss(3.6, 0.7))), 2)
            late_days = max(0, int(random.gauss(3, 2)))
            customer_tickets = max(0, int(random.gauss(14, 7)))
            acquisition_channel = random.choice(channels)

            city_bonus = {
                "Shanghai": 1.15,
                "Beijing": 1.12,
                "Shenzhen": 1.1,
                "Guangzhou": 1.0,
                "Hangzhou": 1.06,
                "Chengdu": 0.95,
            }[city]
            edu_bonus = {"高中": 0.85, "本科": 1.0, "硕士": 1.12, "博士": 1.2}[education]
            dept_bonus = {
                "Sales": 1.0,
                "Product": 1.07,
                "Tech": 1.15,
                "Support": 0.93,
                "Finance": 1.04,
                "HR": 0.9,
            }[department]

            nonlinear = math.sin(projects_last_year / 2.5) * 3200 + math.log1p(years_experience + 1) * 2500
            base_income = (
                18000
                + age * 620
                + years_experience * 1400
                + projects_last_year * 900
                + cert_count * 1300
                + manager_score * 1700
                + nonlinear
            )
            income = int(base_income * city_bonus * edu_bonus * dept_bonus + random.gauss(0, 4500))
            income = max(32000, min(260000, income))

            latent = (
                income / 18000
                + projects_last_year * 0.75
                + manager_score * 1.35
                + satisfaction * 1.1
                + cert_count * 0.5
                + years_experience * 0.2
                - overtime_hours * 0.14
                - late_days * 0.45
                - customer_tickets * 0.03
                + (0.6 if remote_ratio in [40, 60] else -0.2)
                + random.gauss(0, 1.5)
            )

            if latent < 9:
                target_label = "D"
            elif latent < 12.5:
                target_label = "C"
            elif latent < 16:
                target_label = "B"
            else:
                target_label = "A"

            # 加入少量缺失值与异常值，增强真实感。
            if random.random() < 0.03:
                income = ""
            if random.random() < 0.02:
                city = ""
            if random.random() < 0.02:
                manager_score = ""
            if random.random() < 0.015:
                projects_last_year = ""
            if random.random() < 0.01:
                overtime_hours = int(overtime_hours * random.randint(3, 6))

            writer.writerow(
                [
                    age,
                    income,
                    city,
                    department,
                    education,
                    years_experience,
                    projects_last_year,
                    avg_weekly_hours,
                    overtime_hours,
                    cert_count,
                    remote_ratio,
                    satisfaction,
                    manager_score,
                    late_days,
                    customer_tickets,
                    acquisition_channel,
                    target_label,
                ]
            )


if __name__ == "__main__":
    output = Path(__file__).resolve().parent / "demo_complex.csv"
    generate(output)
    print(output)
