#!/usr/bin/env python3
"""Automatic product diagnosis schedule check CLI entry."""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..")))

from _output import print_output
from capabilities.check_auto_diagnosis_schedule.service import check_auto_diagnosis_schedule

COMMAND_NAME = "check_auto_diagnosis_schedule"
COMMAND_DESC = "检查是否已配置1688商品自动体检定时任务"


def main():
    result = check_auto_diagnosis_schedule()
    print_output(True, "定时任务状态检查完成", result)


if __name__ == "__main__":
    main()
