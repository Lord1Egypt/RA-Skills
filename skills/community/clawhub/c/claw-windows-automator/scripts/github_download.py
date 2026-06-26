#!/usr/bin/env python3
# -*- coding: utf-8, -*-

"""
Skill Name: claw-windows-automator
Author: 王岷瑞/https://github.com/wangminrui2022
License: Apache License
Description: github_download 是一个自动化从 GitHub 下载最新发布包的任务模块，专门用于一键打开浏览器并下载指定 GitHub 仓库的最新源码 ZIP 包。
基本信息：
    模块名称：NAME = "github_download"
    功能描述：打开运行 → 浏览器 → 访问传入的GitHub地址 → 自动下载最新发布包
核心功能（execute 函数）：
    该模块通过模拟用户操作，实现全自动打开 GitHub 仓库并下载最新版本源码，整个流程无需手动干预。
执行流程：
    1、准备阶段
        记录日志并更新屏幕渐变提示
        强制切换到英文输入法（避免输入异常）
        获取外部传入的 GitHub 仓库地址（例如：https://github.com/openclaw/openclaw）
    2、打开浏览器并访问仓库首页
        使用 Win + R 打开「运行」窗口
        输入 cmd.exe /c start "" {github_url} 命令，让系统默认浏览器直接打开 GitHub 仓库页面
    3、跳转到最新发布页并解析下载链接
        构造最新版本页面地址：{github_url}/releases/latest
        使用 requests 发起请求，获取实际重定向后的 tag 名称（例如 v1.0.0）
        自动拼接出源码 ZIP 的直链：{github_url}/archive/refs/tags/{latest_tag}.zip
    4、触发下载
        模拟 Ctrl + L 聚焦浏览器地址栏
        输入解析得到的 ZIP 下载直链并按回车
        浏览器会自动开始下载最新版本的源码压缩包
"""
import pyautogui
import gradient_overlay
import pyautogui
import requests

NAME = "github_download"
DESCRIPTION = "打开运行 → 浏览器 → 访问传入的GitHub地址 → 自动下载最新发布包"

def execute(url: str, utils):
    """
    通用 GitHub 最新包下载工作流
    :param work_path: 无用（保留统一接口）
    :param url: 外部传入的 GitHub 地址（例如 https://github.com/openclaw/openclaw）
    :param utils: 引擎工具
    """
    utils.log_info("🚀 启动 GitHub 自动下载工作流")
    gradient_overlay.update_overlay_text("准备打开浏览器")

    # ==========================
    # 关键：从 CLI 参数 --url 传入 GitHub 地址
    # ==========================
    github_url = url.strip()
    utils.log_info(f"目标仓库：{github_url}")
    utils.ensure_english_input()#输入法转英文

    # ==========================
    #  Win+R 打开运行窗口
    # ==========================
    pyautogui.hotkey("win", "r")
    gradient_overlay.safe_sleep(0.8)
    pyautogui.write(f'cmd.exe /c start "" {github_url}', interval=0.12)
    gradient_overlay.safe_sleep(0.5)
    pyautogui.press("enter")

    utils.log_info("✅ 浏览器已打开，等待加载")
    gradient_overlay.safe_sleep(6.0)

    # ==========================
    # 进入最新发布页
    # ==========================
    latest_url = f"{github_url}/releases/latest"
    utils.log_info(f"跳转到最新版本：{latest_url}")
    gradient_overlay.safe_sleep(1.0)
    gradient_overlay.update_overlay_text("开始下载")
    try:
        # 1. 后台解析最新版 ZIP 的真实下载链接
        response = requests.get(latest_url)
        # URL 会被重定向到带有具体 tag 的地址，例如 .../releases/tag/v1.0.0
        latest_tag = response.url.split('/')[-1] 
        zip_download_url = f"{github_url}/archive/refs/tags/{latest_tag}.zip"

        utils.log_info(f"🔗 成功解析直链: {zip_download_url}")

        # 2. 此时浏览器仍在最前端，直接利用地址栏触发下载
        pyautogui.hotkey("ctrl", "l")
        gradient_overlay.safe_sleep(0.6)
        pyautogui.write(zip_download_url, interval=0.05)
        gradient_overlay.safe_sleep(0.5)
        pyautogui.press("enter")

        gradient_overlay.safe_sleep(2.0)
        utils.log_info("✅ 下载已自动开始！")
        
    except Exception as fallback_error:
        utils.log_info(f"❌ 严重错误: {fallback_error}")