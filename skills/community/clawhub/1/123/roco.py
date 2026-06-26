"""
OpenClaw skill 入口
在 OpenClaw 的 skills 目录下放置此文件，或按照你的 OpenClaw 版本注册方式引入
"""
import asyncio
from roco_actions import RocoActions

_game = RocoActions()


def _run(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, coro)
                return future.result()
        return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


def roco_start() -> str:
    """启动洛克王国游戏"""
    return _run(_game.start())


def roco_after_login() -> str:
    """QQ 登录完成后调用，保存登录状态"""
    return _run(_game.after_login())


def roco_observe() -> str:
    """查看当前游戏状态"""
    return _run(_game.observe())


def roco_step() -> str:
    """执行一步游戏操作"""
    return _run(_game.step())


def roco_auto(steps: int = 20) -> str:
    """自动执行 N 步（默认20步），遇到需要手动处理时暂停"""
    return _run(_game.auto_play(int(steps)))


def roco_stop() -> str:
    """停止游戏并关闭浏览器"""
    async def _stop():
        await _game.controller.close()
        return "游戏已停止"
    return _run(_stop())
