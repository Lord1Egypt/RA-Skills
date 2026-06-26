#!/usr/bin/python3
"""gen_data.py - 根据工具名和用户指令列表生成 JSONL 训练数据（新版格式）"""
import sys, os, json, argparse, random

SCENES=["舒适睡眠","回家模式","离家模式","快速净化","烛光晚餐","运动健身",
        "下午茶模式","早餐模式","晚餐模式","看书模式","观影模式","会客模式"]
RMS=["客厅","卧室","书房","厨房","全屋","餐厅","阳台","儿童房"]
ALL_DEVS={
    "空调":["舒享家(空调)","云逸空调(空调)","舒享家Pro(空调)","清风侠(空调)","静心王(空调)","怡然空调(空调)"],
    "窗帘":["客厅窗帘(窗帘)","卧室窗帘(窗帘)","书房窗帘(窗帘)","智能窗帘(窗帘)","电动窗帘(窗帘)"],
    "风扇":["静音风扇(风扇)","智能风扇(风扇)","塔扇(风扇)","落地扇(风扇)","直流风扇(风扇)"],
    "空气净化器":["空气净化器(空气净化器)","除醛净化器(净化器)","智能净化器(净化器)","飞利浦净化器(净化器)"],
    "智能开关":["客厅开关(智能开关)","卧室开关(智能开关)","智能开关(智能开关)","触控开关(开关)"],
    "灯":["客厅灯(灯)","卧室灯(灯)","台灯(灯)","吸顶灯(灯)","氛围灯(灯)","阅读灯(灯)","小夜灯(灯)"],
    "电暖器":["电暖器(电暖器)","踢脚线暖(电暖器)","油汀(电暖器)","暖风机(电暖器)"],
    "净水机":["净水机(净水机)","RO净水机(净水机)","厨下净水机(净水机)","直饮机(净饮机)"],
    "扫地机":["扫地机(扫地机)","扫拖一体机(扫地机)","扫地机器人(扫地机)","米家扫地机(扫地机)"],
    "除湿机":["除湿机(除湿机)","智能除湿机(除湿机)","家用除湿机(除湿机)","德业除湿机(除湿机)"],
    "加湿器":["加湿器(加湿器)","超声波加湿器(加湿器)","智能加湿器(加湿器)","卧室加湿器(加湿器)"],
    "电饭煲":["米香煲(电饭煲)","智能电饭煲(电饭煲)","压力电饭煲(电饭煲)","小电饭煲(电饭煲)"],
    "热水器":["热水器(热水器)","燃气热水器(热水器)","电热水器(热水器)","热水宝(热水器)"],
    "冰箱":["智能冰箱(冰箱)","对开门冰箱(冰箱)","变频冰箱(冰箱)","海尔冰箱(冰箱)"],
    "净饮机":["净饮机(净饮机)","即热净饮机(净饮机)","厨下净饮机(净饮机)","饮水机(饮水机)"],
    "地暖转接器":["地暖转接器(地暖转接器)","智能地暖(地暖)","温控器(温控)"],
    "壁挂炉":["壁挂炉(壁挂炉)","燃气壁挂炉(壁挂炉)","采暖炉(壁挂炉)"],
    "智能插座":["智能插座(智能插座)","wifi插座(插座)","定时插座(插座)"],
    "新风机":["新风机(新风机)","智能新风机(新风机)","壁挂新风机(新风机)","双向流新风机(新风机)"],
    "油烟机":["油烟机(油烟机)","智能油烟机(油烟机)","侧吸油烟机(油烟机)","顶吸油烟机(油烟机)"],
    "洗碗机":["洗碗机(洗碗机)","智能洗碗机(洗碗机)","嵌入式洗碗机(洗碗机)","台式洗碗机(洗碗机)"],
    "热水发生器":["热水发生器(热水发生器)","燃气热水(热水)","即热式热水(热水)"],
    "软水机":["软水机(软水机)","中央软水机(软水机)","厨房软水机(软水机)","柔水宝(软水机)"],
    "饮水机":["饮水机(饮水机)","智能饮水机(饮水机)","净饮一体机(净饮机)","立式饮水机(饮水机)"],
    "蒸烤机":["蒸烤机(蒸烤机)","蒸烤箱(蒸烤机)","嵌入式蒸烤箱(蒸烤机)","台式蒸烤机(蒸烤机)"],
    "洗衣机":["海尔洗衣机(洗衣机)","滚筒洗衣机(洗衣机)","洗烘一体机(洗衣机)","智能洗衣机(洗衣机)"],
}
ALL_DEV_LIST=[n for v in ALL_DEVS.values() for n in v]

def rt():
    y=random.choice([2026,2027])
    return f"{y}-{random.randint(1,12):02d}-{random.randint(1,28):02d} {random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"
def scenes():
    return [{"scene_id":random.randint(65000,66000),"scene_name":random.choice(SCENES),"room_name":random.choice(RMS)} for _ in range(random.randint(2,4))]
def ld():
    return random.choice(ALL_DEV_LIST)
def dl(ld_str):
    count=random.randint(8,18)
    room=random.choice(RMS)
    others=[n for n in ALL_DEV_LIST if n!=ld_str]
    sel=[ld_str]+random.sample(others,min(count-1,len(others)))
    random.shuffle(sel)
    n_room=random.randint(2,4)
    rooms=random.sample(RMS,n_room)
    per=len(sel)//n_room
    res={}; start=0
    for i,r in enumerate(rooms):
        end=start+per+(1 if i<n_room-1 else len(sel)-start-per*(n_room-1))
        res[r]=sel[start:end]; start=end
    return res
def ctx(instr,ld_str):
    return (f"<当前用户指令>{instr}</当前用户指令>\n"
            f"<本地设备>{ld_str}</本地设备>\n"
            f"<当前时间>{rt()}</当前时间>\n"
            f"<用户场景列表>{json.dumps(scenes(),ensure_ascii=False)}</用户场景列表>\n"
            f"<用户设备列表>{json.dumps(dl(ld_str),ensure_ascii=False)}</用户设备列表>")

def tc_json(**kwargs):
    return "<tool_call>" + json.dumps(kwargs, ensure_ascii=False) + "</tool_call>"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("tool_name")
    p.add_argument("output_file")
    p.add_argument("-i","--instructions")
    p.add_argument("-f","--file")
    p.add_argument("--city",default="")
    args=p.parse_args()

    if args.instructions:
        instrs=[u.strip() for u in args.instructions.split(",") if u.strip()]
    elif args.file and os.path.exists(args.file):
        with open(args.file,encoding="utf-8") as f:
            instrs=[l.strip() for l in f if l.strip()]
    else:
        print("错误: 请通过 --instructions 或 --file 提供用户指令"); sys.exit(1)

    print(f"[gen_data] 工具={args.tool_name}  指令数={len(instrs)}")

    results=[]
    for instr in instrs:
        ldv=ld()
        dn=ldv.rsplit("(",1)[0]
        tool=args.tool_name
        convs=None

        if tool=="dev_control":
            convs=[{"from":"human","value":ctx(instr,ldv)},
                   {"from":"assistant","value":tc_json(tool_name="dev_control",query=instr)},
                   {"from":"observation","value":"<tool_response>操作成功。</tool_response>"},
                   {"from":"assistant","value":f"{dn}已执行完成~"}]
        elif tool=="scene_generator":
            convs=[{"from":"human","value":ctx(instr,ldv)},
                   {"from":"assistant","value":tc_json(tool_name="scene_generator",command=f"打开{dn}",name=f"打开{dn}场景",repeat_type="single",datetime="",custom_days="",condition="")},
                   {"from":"observation","value":"<tool_response>场景创建成功。</tool_response>"},
                   {"from":"assistant","value":f"好的，{dn}场景已创建好啦~"}]
        elif tool=="weather":
            city=args.city or ""
            convs=[{"from":"human","value":ctx(instr,ldv)},
                   {"from":"assistant","value":tc_json(tool_name="weather",city=city)},
                   {"from":"observation","value":"<tool_response>天气查询成功，当前天气晴，气温26度。</tool_response>"},
                   {"from":"assistant","value":f"当前{city or '本地'}天气晴朗，气温26度，适宜出行~"}]
        elif tool=="alarm_remind":
            convs=[{"from":"human","value":ctx(instr,ldv)},
                   {"from":"assistant","value":tc_json(tool_name="alarm_remind",alarm_ids=[],action="add",alarm_type="reminder",label="提醒",repeat_type="single",custom_days=[],time="2026-03-21 20:00:00")},
                   {"from":"observation","value":"<tool_response>提醒设置成功。</tool_response>"},
                   {"from":"assistant","value":"好的，提醒已设置好啦~"}]
        elif tool=="dev_info":
            dlj=json.dumps(dl(ldv),ensure_ascii=False)
            convs=[{"from":"human","value":ctx(instr,ldv)},
                   {"from":"assistant","value":"<tool_call>{\"tool_name\":\"dev_info\"}</tool_call>"},
                   {"from":"observation","value":"<tool_call>"+dlj+"</tool_call>"},
                   {"from":"assistant","value":"家里共发现多台设备，涵盖空调、灯、窗帘等多种类型~"}]
        elif tool=="scene_control":
            convs=[{"from":"human","value":ctx(instr,ldv)},
                   {"from":"assistant","value":tc_json(tool_name="scene_control",scene_id=1001)},
                   {"from":"observation","value":"<tool_response>场景开启成功。</tool_response>"},
                   {"from":"assistant","value":"场景已开启~"}]
        elif tool=="exit_dialog":
            convs=[{"from":"human","value":ctx(instr,ldv)},
                   {"from":"assistant","value":"<tool_call>{\"tool_name\":\"exit_dialog\"}</tool_call>"},
                   {"from":"observation","value":"<tool_response>退出对话。</tool_response>"},
                   {"from":"assistant","value":"好的，再见啦~"}]
        elif tool=="GreeQA":
            convs=[{"from":"human","value":ctx(instr,ldv)},
                   {"from":"assistant","value":tc_json(tool_name="GreeQA",query=instr)},
                   {"from":"observation","value":"<tool_response>根据知识库查询结果回答。</tool_response>"},
                   {"from":"assistant","value":"根据知识库，这是您需要的相关信息~"}]
        elif tool=="scene_guide":
            convs=[{"from":"human","value":ctx(instr,ldv)},
                   {"from":"assistant","value":"<tool_call>{\"tool_name\":\"scene_guide\"}</tool_call>"},
                   {"from":"observation","value":"<tool_response>场景查询成功，共5个场景。</tool_response>"},
                   {"from":"assistant","value":"当前共有5个场景，已为您列出~"}]
        elif tool=="chat":
            convs=[{"from":"human","value":ctx(instr,ldv)},
                   {"from":"assistant","value":"<tool_call>{\"tool_name\":\"chat\"}</tool_call>"},
                   {"from":"observation","value":"<tool_response>闲聊回复。</tool_response>"},
                   {"from":"assistant","value":"这个话题我帮您聊聊~"}]
        else:
            print(f"未知工具: {tool}"); sys.exit(1)

        results.append({"conversations":convs,"system":"","history":[]})

    with open(args.output_file,"w",encoding="utf-8") as f:
        for r in results: f.write(json.dumps(r,ensure_ascii=False)+"\n")
    print(f"[gen_data] 完成! {len(results)}条 -> {args.output_file}")
    if results:
        print("\n=== 样例 ===")
        for c in results[0]["conversations"]:
            print(f"  [{c['from']}] {c['value'][:120]}")

if __name__=="__main__":
    main()
