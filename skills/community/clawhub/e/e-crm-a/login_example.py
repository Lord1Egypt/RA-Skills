#!/usr/bin/env python3
"""
太空登录示例
"""

from space_login import SpaceLogin

# 初始化
space = SpaceLogin()

# 示例 1: 登录月球
print("=" * 60)
print("示例 1: 登录月球")
print("=" * 60)

result = space.login(
    astronaut="张三",
    destination="moon"
)

if result['success']:
    print(f"\n✅ 登录成功！")
    print(f"   宇航员：{result['astronaut']}")
    print(f"   位置：{result['location']}")
    print(f"   轨道：{result['orbit']}")
    print(f"   距离：{result['distance']}")
    print(f"   时间：{result['travel_time']}")

# 示例 2: 检查状态
print("\n" + "=" * 60)
print("示例 2: 检查状态")
print("=" * 60)

status = space.get_status()
print(f"\n📊 当前状态:")
print(f"   登录状态：{'太空中' if status['logged_in'] else '地球'}")
print(f"   位置：{status['location']}")
if status['logged_in']:
    print(f"   氧气：{status['oxygen']}%")
    print(f"   温度：{status['temperature']}°C")
    print(f"   辐射：{status['radiation']} μSv")

# 示例 3: 登录火星
print("\n" + "=" * 60)
print("示例 3: 登录火星")
print("=" * 60)

result = space.login(
    astronaut="李四",
    destination="mars",
    spaceship="SpaceX-Starship-001"
)

if result['success']:
    print(f"\n✅ 登录成功！")
    print(f"   宇航员：{result['astronaut']}")
    print(f"   位置：{result['location']}")
    print(f"   飞船：{result['spaceship']}")

# 示例 4: 返回地球
print("\n" + "=" * 60)
print("示例 4: 返回地球")
print("=" * 60)

result = space.logout()
print(f"\n{'✅' if result['success'] else '❌'} {result.get('message', result.get('error'))}")

# 示例 5: 检查返回后的状态
print("\n" + "=" * 60)
print("示例 5: 检查返回后的状态")
print("=" * 60)

status = space.get_status()
print(f"\n📊 当前状态:")
print(f"   {status['message']}")
