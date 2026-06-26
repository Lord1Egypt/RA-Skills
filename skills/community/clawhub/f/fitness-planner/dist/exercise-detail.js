// 动作详细讲解库
// ==================== 胸部动作 ====================
export const exerciseDetails = [
    // 胸部
    {
        name: '卧推',
        aliases: ['杠铃卧推', '平板卧推', 'bench press'],
        category: 'chest',
        equipment: ['杠铃', '卧推凳'],
        difficulty: 'intermediate',
        steps: [
            '平躺在卧推凳上，双脚踩稳地面',
            '双手握杠，握距略宽于肩',
            '下放杠铃至胸部中段，手肘约45°角',
            '推起杠铃至手臂伸直，顶峰收缩胸肌'
        ],
        tips: [
            '收紧肩胛骨，胸部挺起',
            '下放时吸气，推起时呼气',
            '手腕保持中立，不要过度后伸'
        ],
        commonErrors: [
            '手肘外展90°，容易伤肩',
            '起桥过高，借力腰腹',
            '下放位置不对，太高或太低'
        ],
        videoSearchKeywords: '卧推动作教学'
    },
    {
        name: '哑铃卧推',
        aliases: ['平板哑铃卧推', '地板哑铃卧推', 'dumbbell bench press'],
        category: 'chest',
        equipment: ['哑铃'],
        difficulty: 'beginner',
        steps: [
            '平躺，双脚踩稳地面，哑铃位于胸部两侧',
            '手肘约45°角，大臂与躯干呈45°',
            '推起哑铃至胸肌上方，双臂伸直',
            '缓慢下放至大臂接近地面'
        ],
        tips: [
            '推起时想象抱一棵大树，向中间挤压',
            '控制离心，下放比推起更慢',
            '地板卧推时下放至大臂触地即可'
        ],
        commonErrors: [
            '手肘外展90°',
            '哑铃碰撞，失去控制',
            '下放不够深'
        ],
        videoSearchKeywords: '哑铃卧推动作教学'
    },
    {
        name: '上斜哑铃卧推',
        aliases: ['上斜卧推', 'inclined dumbbell press'],
        category: 'chest',
        equipment: ['哑铃', '上斜凳'],
        difficulty: 'intermediate',
        steps: [
            '调节凳子角度30-45°',
            '坐姿，哑铃放在大腿上，借助腿部力量举至肩部',
            '推起哑铃至锁骨上方，手臂伸直',
            '缓慢下放至上胸位置'
        ],
        tips: [
            '角度不要超过45°，否则三角肌前束参与过多',
            '下放至肘部低于躯干',
            '顶峰挤压上胸1秒'
        ],
        commonErrors: [
            '角度太高变成肩推',
            '下放位置偏下，刺激中胸',
            '重量过大导致借力'
        ],
        videoSearchKeywords: '上斜哑铃卧推教学'
    },
    {
        name: '哑铃飞鸟',
        aliases: ['平板飞鸟', 'dumbbell fly'],
        category: 'chest',
        equipment: ['哑铃'],
        difficulty: 'beginner',
        steps: [
            '平躺，双臂伸直举起哑铃，掌心相对',
            '手臂微弯保持固定角度（约20°）',
            '向两侧下放，感受胸肌拉伸',
            '沿弧线向上合拢，像抱一棵大树'
        ],
        tips: [
            '手臂角度固定不变，不要变弯伸直',
            '感受胸肌拉伸，不要用手臂发力',
            '顶峰挤压胸肌1秒'
        ],
        commonErrors: [
            '手臂伸直锁定，肘关节压力大',
            '做成了卧推动作',
            '重量过大无法控制'
        ],
        videoSearchKeywords: '哑铃飞鸟正确姿势'
    },
    {
        name: '俯卧撑',
        aliases: ['标准俯卧撑', 'push up'],
        category: 'chest',
        equipment: [],
        difficulty: 'beginner',
        steps: [
            '双手撑地，距离略宽于肩',
            '身体成一直线，核心收紧',
            '下放至胸部接近地面',
            '推起至手臂伸直'
        ],
        tips: [
            '手肘约45°角，不要外展90°',
            '核心始终收紧，不要塌腰',
            '下放时吸气，推起时呼气'
        ],
        commonErrors: [
            '塌腰或撅臀',
            '手肘外展',
            '下放不够深'
        ],
        videoSearchKeywords: '俯卧撑正确姿势教学'
    },
    {
        name: '下斜俯卧撑',
        aliases: ['上胸俯卧撑', 'decline push up'],
        category: 'chest',
        equipment: [],
        difficulty: 'intermediate',
        steps: [
            '双脚放在高处（沙发/床沿/椅子）',
            '双手撑地，距离略宽于肩',
            '身体呈下斜角度，核心收紧',
            '下放至胸部接近地面，推起'
        ],
        tips: [
            '更多刺激上胸',
            '脚放得越高，难度越大',
            '身体保持一条直线'
        ],
        commonErrors: [
            '塌腰',
            '手肘外展',
            '下放不够深'
        ],
        videoSearchKeywords: '下斜俯卧撑动作教学'
    },
    {
        name: '窄距俯卧撑',
        aliases: ['钻石俯卧撑', 'diamond push up', '三头俯卧撑'],
        category: 'triceps',
        equipment: [],
        difficulty: 'intermediate',
        steps: [
            '双手并拢，食指和拇指围成菱形/钻石形',
            '手位于胸部正下方',
            '手肘贴近身体向后',
            '下放至胸部接近手背，推起'
        ],
        tips: [
            '主要刺激三头肌',
            '手肘向后，不要外展',
            '太难可以膝盖着地'
        ],
        commonErrors: [
            '手肘外展',
            '塌腰',
            '手的位置太靠前或靠后'
        ],
        videoSearchKeywords: '窄距俯卧撑钻石俯卧撑教学'
    },
    // 背部
    {
        name: '引体向上',
        aliases: ['正手引体向上', 'pull up'],
        category: 'back',
        equipment: ['单杠'],
        difficulty: 'advanced',
        steps: [
            '双手正握单杠，握距略宽于肩',
            '悬挂，手臂伸直，肩胛骨下沉',
            '拉起身体至下巴过杠',
            '缓慢下放至手臂伸直'
        ],
        tips: [
            '先学会肩胛骨下沉',
            '想象用肘部向下拉，而不是用手',
            '控制下放，不要晃动'
        ],
        commonErrors: [
            '借力晃动',
            '下放不充分',
            '耸肩拉'
        ],
        videoSearchKeywords: '引体向上动作教学'
    },
    {
        name: '反手引体向上',
        aliases: ['反握引体向上', 'chin up', '二头引体'],
        category: 'biceps',
        equipment: ['单杠'],
        difficulty: 'intermediate',
        steps: [
            '双手反握单杠，握距与肩同宽或略窄',
            '悬挂，手臂伸直',
            '拉起身体至下巴过杠',
            '缓慢下放'
        ],
        tips: [
            '二头肌参与更多，适合练手臂',
            '比正手引体更容易',
            '顶峰挤压二头肌'
        ],
        commonErrors: [
            '借力晃动',
            '下放不充分',
            '握距太宽'
        ],
        videoSearchKeywords: '反手引体向上二头肌教学'
    },
    {
        name: '高位下拉',
        aliases: ['坐姿下拉', 'lat pulldown'],
        category: 'back',
        equipment: ['高位下拉机'],
        difficulty: 'beginner',
        steps: [
            '坐姿，大腿固定在挡板下',
            '双手宽握横杆，身体微后倾',
            '下拉至锁骨位置，挤压背阔肌',
            '缓慢回放'
        ],
        tips: [
            '想象用肘部下拉',
            '不要过度后仰借力',
            '顶峰收缩1秒'
        ],
        commonErrors: [
            '拉到颈后（容易伤肩）',
            '过度后仰',
            '回放太快'
        ],
        videoSearchKeywords: '高位下拉动作教学'
    },
    {
        name: '杠铃划船',
        aliases: ['俯身划船', 'barbell row'],
        category: 'back',
        equipment: ['杠铃'],
        difficulty: 'intermediate',
        steps: [
            '双脚与肩同宽，俯身约45°',
            '双手握杠，握距略宽于肩',
            '拉起杠铃至下腹部，挤压背部',
            '缓慢下放'
        ],
        tips: [
            '保持背部平直，不要弓背',
            '拉向腹部而不是胸部',
            '肘部贴近身体'
        ],
        commonErrors: [
            '弓背',
            '站太直',
            '借力晃动'
        ],
        videoSearchKeywords: '杠铃划船动作教学'
    },
    {
        name: '哑铃划船',
        aliases: ['单臂哑铃划船', 'dumbbell row'],
        category: 'back',
        equipment: ['哑铃', '凳子'],
        difficulty: 'beginner',
        steps: [
            '一只手和膝盖放在凳子上支撑',
            '另一只手持哑铃，手臂自然下垂',
            '拉起哑铃至腰侧，挤压背部',
            '缓慢下放'
        ],
        tips: [
            '背部保持平直',
            '拉向髋部而不是肩部',
            '感受背阔肌收缩'
        ],
        commonErrors: [
            '扭转身体借力',
            '拉得太高变成后束',
            '下放不充分'
        ],
        videoSearchKeywords: '哑铃划船动作教学'
    },
    // 肩部
    {
        name: '肩推',
        aliases: ['站姿肩推', '坐姿肩推', 'overhead press', 'military press'],
        category: 'shoulder',
        equipment: ['杠铃/哑铃'],
        difficulty: 'intermediate',
        steps: [
            '站姿或坐姿，杠铃/哑铃位于肩部',
            '推起至手臂伸直，杠铃在头顶',
            '缓慢下放至锁骨/肩部位置'
        ],
        tips: [
            '核心收紧，不要过度后仰',
            '推起时稍微后仰，下放时回正',
            '手腕保持中立'
        ],
        commonErrors: [
            '过度后仰借力',
            '下放位置太低',
            '手腕过度后伸'
        ],
        videoSearchKeywords: '肩推动作教学'
    },
    {
        name: '哑铃侧平举',
        aliases: ['侧平举', 'lateral raise'],
        category: 'shoulder',
        equipment: ['哑铃'],
        difficulty: 'beginner',
        steps: [
            '双手持哑铃，放在身体两侧',
            '向两侧举起至与肩同高',
            '顶峰停留1秒，缓慢下放'
        ],
        tips: [
            '手臂微弯，固定角度',
            '小指略高，激活中束',
            '不要耸肩'
        ],
        commonErrors: [
            '举得太高超过肩',
            '耸肩借力',
            '重量过大甩动'
        ],
        videoSearchKeywords: '哑铃侧平举正确姿势'
    },
    {
        name: '哑铃前平举',
        aliases: ['前平举', 'front raise'],
        category: 'shoulder',
        equipment: ['哑铃'],
        difficulty: 'beginner',
        steps: [
            '双手持哑铃，放在大腿前方',
            '举起哑铃至视线高度',
            '缓慢下放'
        ],
        tips: [
            '手臂微弯',
            '左右交替或同时进行',
            '控制离心'
        ],
        commonErrors: [
            '甩动借力',
            '下放太快',
            '举得太高'
        ],
        videoSearchKeywords: '哑铃前平举动作教学'
    },
    {
        name: '俯身飞鸟',
        aliases: ['反向飞鸟', 'rear delt fly', '后束飞鸟'],
        category: 'shoulder',
        equipment: ['哑铃'],
        difficulty: 'beginner',
        steps: [
            '俯身约45°，双手持哑铃自然下垂',
            '向两侧举起哑铃，手臂微弯',
            '顶峰挤压后束，缓慢下放'
        ],
        tips: [
            '专注后束，不要用背阔肌借力',
            '小指略高',
            '动作要慢'
        ],
        commonErrors: [
            '站起来变成侧平举',
            '借力背部',
            '重量过大'
        ],
        videoSearchKeywords: '俯身飞鸟后束训练'
    },
    {
        name: '面拉',
        aliases: ['绳索面拉', 'face pull'],
        category: 'shoulder',
        equipment: ['绳索'],
        difficulty: 'beginner',
        steps: [
            '绳索调至面部高度',
            '双手握住绳索两端',
            '拉向面部，双手向两侧展开',
            '顶峰挤压后束和肩胛骨'
        ],
        tips: [
            '拉向面部，不是胸部',
            '肩胛骨后缩',
            '控制回放'
        ],
        commonErrors: [
            '拉向胸部',
            '重量过大',
            '回放太快'
        ],
        videoSearchKeywords: '面拉动作教学'
    },
    // 腿部
    {
        name: '深蹲',
        aliases: ['杠铃深蹲', 'back squat', 'squat'],
        category: 'leg',
        equipment: ['杠铃'],
        difficulty: 'intermediate',
        steps: [
            '杠铃放在斜方肌上，双脚与肩同宽',
            '臀部向后坐，膝盖沿脚尖方向',
            '下蹲至大腿至少平行地面',
            '起身站直'
        ],
        tips: [
            '膝盖方向与脚尖一致',
            '重心在脚后跟和脚掌外侧',
            '核心收紧，背部挺直'
        ],
        commonErrors: [
            '膝盖内扣',
            '弯腰弓背',
            '踮脚尖'
        ],
        videoSearchKeywords: '深蹲动作教学'
    },
    {
        name: '高脚杯深蹲',
        aliases: ['杯式深蹲', 'goblet squat'],
        category: 'leg',
        equipment: ['哑铃/壶铃'],
        difficulty: 'beginner',
        steps: [
            '双手托住哑铃/壶铃在胸前',
            '双脚略宽于肩，脚尖略外展',
            '下蹲至大腿平行地面',
            '起身站直'
        ],
        tips: [
            '适合新手学习深蹲模式',
            '哑铃帮助保持躯干直立',
            '手肘在大腿内侧帮助打开髋部'
        ],
        commonErrors: [
            '弯腰',
            '膝盖内扣',
            '踮脚尖'
        ],
        videoSearchKeywords: '高脚杯深蹲教学'
    },
    {
        name: '哑铃深蹲',
        aliases: ['双手持铃深蹲'],
        category: 'leg',
        equipment: ['哑铃'],
        difficulty: 'beginner',
        steps: [
            '双手各持一个哑铃，放在身体两侧',
            '双脚与肩同宽',
            '下蹲至大腿至少平行地面',
            '起身站直'
        ],
        tips: [
            '适合居家训练',
            '哑铃可以放在肩上',
            '核心收紧'
        ],
        commonErrors: [
            '弯腰',
            '膝盖内扣',
            '下蹲不够深'
        ],
        videoSearchKeywords: '哑铃深蹲教学'
    },
    {
        name: '罗马尼亚硬拉',
        aliases: ['RDL', 'romanian deadlift'],
        category: 'leg',
        equipment: ['杠铃/哑铃'],
        difficulty: 'intermediate',
        steps: [
            '双手持杠铃/哑铃，站直',
            '臀部后推，膝盖微弯保持固定',
            '下放至大腿后侧有拉伸感',
            '髋部前推站起'
        ],
        tips: [
            '膝盖角度固定不变',
            '感受腘绳肌拉伸',
            '背部保持平直'
        ],
        commonErrors: [
            '变成深蹲',
            '弯腰弓背',
            '膝盖过度弯曲'
        ],
        videoSearchKeywords: '罗马尼亚硬拉教学'
    },
    {
        name: '腿举',
        aliases: ['倒蹬机', 'leg press'],
        category: 'leg',
        equipment: ['腿举机'],
        difficulty: 'beginner',
        steps: [
            '坐在腿举机上，双脚放在踏板上',
            '双脚与肩同宽，脚尖略外展',
            '下放踏板至膝盖90°',
            '推起踏板'
        ],
        tips: [
            '脚放得高更多刺激臀部/腘绳肌',
            '脚放得低更多刺激股四头',
            '不要锁死膝盖'
        ],
        commonErrors: [
            '下放不够深',
            '锁死膝盖',
            '重量过大臀部离开凳子'
        ],
        videoSearchKeywords: '腿举动作教学'
    },
    {
        name: '腿弯举',
        aliases: ['俯卧腿弯举', 'leg curl'],
        category: 'leg',
        equipment: ['腿弯举机'],
        difficulty: 'beginner',
        steps: [
            '俯卧在腿弯举机上',
            '脚后跟钩住滚轴',
            '弯曲膝盖，脚后跟向臀部',
            '缓慢下放'
        ],
        tips: [
            '孤立刺激腘绳肌',
            '顶峰收缩1秒',
            '不要过度拱腰'
        ],
        commonErrors: [
            '下放太快',
            '借力拱腰',
            '幅度不够'
        ],
        videoSearchKeywords: '腿弯举动作教学'
    },
    {
        name: '弓步蹲',
        aliases: ['箭步蹲', 'lunge'],
        category: 'leg',
        equipment: ['哑铃/自重'],
        difficulty: 'beginner',
        steps: [
            '双脚并拢站立',
            '一只脚向前迈出一大步',
            '下蹲至后膝接近地面',
            '前脚蹬地回到起始位置'
        ],
        tips: [
            '前膝不要超过脚尖太多',
            '躯干保持直立',
            '可以行走式或原地式'
        ],
        commonErrors: [
            '步幅太小变成窄距蹲',
            '前膝内扣',
            '后膝着地'
        ],
        videoSearchKeywords: '弓步蹲箭步蹲教学'
    },
    {
        name: '臀桥',
        aliases: ['臀推', 'glute bridge', 'hip thrust'],
        category: 'leg',
        equipment: ['自重/杠铃/哑铃'],
        difficulty: 'beginner',
        steps: [
            '仰卧，双脚踩地，膝盖弯曲',
            '臀部收紧，向上挺起',
            '顶峰挤压臀肌2秒',
            '缓慢下放'
        ],
        tips: [
            '专注臀部收缩',
            '顶峰时髋部充分伸展',
            '不要过度拱腰'
        ],
        commonErrors: [
            '用腰发力',
            '顶峰不挤压',
            '下放太快'
        ],
        videoSearchKeywords: '臀桥臀推教学'
    },
    {
        name: '提踵',
        aliases: ['站姿提踵', 'calf raise'],
        category: 'leg',
        equipment: ['自重/器械'],
        difficulty: 'beginner',
        steps: [
            '站在台阶边缘或平地',
            '脚后跟下放低于脚尖',
            '踮起脚尖至最高点',
            '缓慢下放'
        ],
        tips: [
            '顶峰停留1秒',
            '完全拉伸完全收缩',
            '可以单腿增加强度'
        ],
        commonErrors: [
            '幅度太小',
            '做得太快',
            '借力弹跳'
        ],
        videoSearchKeywords: '提踵小腿训练'
    },
    // 二头肌
    {
        name: '杠铃弯举',
        aliases: ['杠铃二头弯举', 'barbell curl'],
        category: 'biceps',
        equipment: ['杠铃'],
        difficulty: 'beginner',
        steps: [
            '双手握杠铃，握距与肩同宽',
            '手臂伸直，杠铃在大腿前',
            '弯举杠铃至肩部，挤压二头肌',
            '缓慢下放'
        ],
        tips: [
            '手肘固定在身体两侧',
            '不要晃动身体借力',
            '顶峰收缩1秒'
        ],
        commonErrors: [
            '晃动借力',
            '手肘前移',
            '下放不充分'
        ],
        videoSearchKeywords: '杠铃弯举动作教学'
    },
    {
        name: '哑铃弯举',
        aliases: ['哑铃二头弯举', 'dumbbell curl'],
        category: 'biceps',
        equipment: ['哑铃'],
        difficulty: 'beginner',
        steps: [
            '双手持哑铃，手臂自然下垂',
            '弯举哑铃，过程中旋转手腕',
            '顶峰掌心朝向自己，挤压二头肌',
            '缓慢下放'
        ],
        tips: [
            '可以交替或同时',
            '手肘固定',
            '控制离心'
        ],
        commonErrors: [
            '晃动借力',
            '手肘前移',
            '下放太快'
        ],
        videoSearchKeywords: '哑铃弯举动作教学'
    },
    {
        name: '锤式弯举',
        aliases: ['对握弯举', 'hammer curl'],
        category: 'biceps',
        equipment: ['哑铃'],
        difficulty: 'beginner',
        steps: [
            '双手持哑铃，掌心相对（对握）',
            '弯举哑铃至肩部',
            '顶峰挤压肱肌',
            '缓慢下放'
        ],
        tips: [
            '更多刺激肱肌和前臂',
            '手肘固定',
            '可以交替或同时'
        ],
        commonErrors: [
            '晃动借力',
            '手腕旋转',
            '下放太快'
        ],
        videoSearchKeywords: '锤式弯举教学'
    },
    {
        name: '集中弯举',
        aliases: ['坐姿集中弯举', 'concentration curl'],
        category: 'biceps',
        equipment: ['哑铃'],
        difficulty: 'beginner',
        steps: [
            '坐姿，双脚分开，持哑铃的手肘抵在大腿内侧',
            '弯举哑铃，挤压二头肌',
            '顶峰停留1秒',
            '缓慢下放'
        ],
        tips: [
            '专注二头肌峰值',
            '不要借力',
            '动作要慢'
        ],
        commonErrors: [
            '借力推大腿',
            '下放太快',
            '手肘离开大腿'
        ],
        videoSearchKeywords: '集中弯举教学'
    },
    {
        name: '21响礼炮',
        aliases: ['21s', '21 gun salute'],
        category: 'biceps',
        equipment: ['杠铃/哑铃'],
        difficulty: 'intermediate',
        steps: [
            '下半程7次：从手臂伸直到小臂平行地面',
            '上半程7次：从小臂平行地面到肩部',
            '全程7次：从完全伸直到肩部'
        ],
        tips: [
            '三个部分各做7次，共21次',
            '每个阶段都充分收缩和拉伸',
            '重量要比正常弯举轻'
        ],
        commonErrors: [
            '偷懒减少幅度',
            '休息时间过长',
            '重量过大'
        ],
        videoSearchKeywords: '21响礼炮二头训练'
    },
    {
        name: '哑铃交替弯举',
        aliases: ['交替弯举'],
        category: 'biceps',
        equipment: ['哑铃'],
        difficulty: 'beginner',
        steps: [
            '双手持哑铃，手臂自然下垂',
            '一只手弯举至肩部',
            '下放的同时另一只手弯举',
            '交替进行'
        ],
        tips: [
            '保持节奏',
            '手肘固定',
            '顶峰旋转手腕'
        ],
        commonErrors: [
            '晃动身体',
            '手肘前移',
            '下放太快'
        ],
        videoSearchKeywords: '哑铃交替弯举教学'
    },
    // 三头肌
    {
        name: '绳索下压',
        aliases: ['三头下压', 'tricep pushdown', 'cable pushdown'],
        category: 'triceps',
        equipment: ['绳索'],
        difficulty: 'beginner',
        steps: [
            '双手握住绳索附件，上臂固定在身体两侧',
            '下压绳索至手臂伸直',
            '顶峰挤压三头肌',
            '缓慢回放'
        ],
        tips: [
            '上臂保持不动',
            '身体不要前倾',
            '可以用直杆、绳索或V杆'
        ],
        commonErrors: [
            '上臂跟着动',
            '身体前倾借力',
            '回放太快'
        ],
        videoSearchKeywords: '绳索下压三头肌教学'
    },
    {
        name: '窄握卧推',
        aliases: ['窄距卧推', 'close grip bench press'],
        category: 'triceps',
        equipment: ['杠铃'],
        difficulty: 'intermediate',
        steps: [
            '双手握杠，握距与肩同宽或略窄',
            '下放杠铃至下胸部',
            '推起至手臂伸直'
        ],
        tips: [
            '手肘贴近身体',
            '握距不要太窄，伤手腕',
            '三头肌主导'
        ],
        commonErrors: [
            '握距太窄',
            '手肘外展',
            '重量过大'
        ],
        videoSearchKeywords: '窄握卧推三头肌教学'
    },
    {
        name: '仰卧臂屈伸',
        aliases: ['三头臂屈伸', 'skull crusher', 'lying tricep extension'],
        category: 'triceps',
        equipment: ['杠铃/哑铃/曲杆'],
        difficulty: 'intermediate',
        steps: [
            '仰卧，双手持杠铃/哑铃在胸前伸直',
            '保持上臂固定，弯曲手肘下放至额头/头后',
            '伸直手臂回到起始位置'
        ],
        tips: [
            '上臂保持垂直不动',
            '用曲杆减少手腕压力',
            '可以下放到头后，拉伸更长'
        ],
        commonErrors: [
            '上臂跟着动',
            '下放太高变成卧推',
            '重量过大'
        ],
        videoSearchKeywords: '仰卧臂屈伸教学'
    },
    {
        name: '哑铃颈后臂屈伸',
        aliases: ['颈后三头屈伸', 'overhead tricep extension'],
        category: 'triceps',
        equipment: ['哑铃'],
        difficulty: 'beginner',
        steps: [
            '双手托住一个哑铃，举过头顶',
            '上臂固定在头部两侧不动',
            '弯曲手肘，下放哑铃至脑后',
            '伸直手臂回到起始位置'
        ],
        tips: [
            '上臂保持不动',
            '可以坐姿或站姿',
            '单手也可以做'
        ],
        commonErrors: [
            '上臂外展',
            '晃动身体',
            '下放幅度不够'
        ],
        videoSearchKeywords: '哑铃颈后臂屈伸教学'
    },
    {
        name: '双杠臂屈伸',
        aliases: ['臂屈伸', 'dip'],
        category: 'triceps',
        equipment: ['双杠'],
        difficulty: 'intermediate',
        steps: [
            '双手撑在双杠上，手臂伸直',
            '身体前倾（更多刺激胸）或直立（更多刺激三头）',
            '下放至肩部低于手肘',
            '推起至手臂伸直'
        ],
        tips: [
            '身体直立=三头肌主导',
            '身体前倾=胸肌主导',
            '太累可以用辅助器械'
        ],
        commonErrors: [
            '下放不够深',
            '耸肩',
            '身体过度前倾（如果目标是三头）'
        ],
        videoSearchKeywords: '双杠臂屈伸教学'
    },
    // 核心
    {
        name: '平板支撑',
        aliases: ['plank', '支撑'],
        category: 'core',
        equipment: [],
        difficulty: 'beginner',
        steps: [
            '前臂和脚尖支撑身体',
            '身体成一条直线，从头到脚',
            '核心收紧，臀部不要下沉或翘起',
            '保持呼吸，不要憋气'
        ],
        tips: [
            '想象有人在要打你肚子，提前收紧',
            '肩膀在手肘正上方',
            '目光看向地面'
        ],
        commonErrors: [
            '塌腰',
            '撅臀',
            '憋气'
        ],
        videoSearchKeywords: '平板支撑正确姿势'
    },
    {
        name: '卷腹',
        aliases: ['仰卧起坐', 'crunch'],
        category: 'core',
        equipment: [],
        difficulty: 'beginner',
        steps: [
            '仰卧，膝盖弯曲，双脚踩地',
            '双手放胸前或耳侧',
            '卷起上背部，下背部贴地',
            '挤压腹肌，缓慢下放'
        ],
        tips: [
            '卷起而不是坐起',
            '下背部始终贴地',
            '不要抱头用力拉脖子'
        ],
        commonErrors: [
            '完全坐起来',
            '抱头用力拉脖子',
            '下放太快'
        ],
        videoSearchKeywords: '卷腹正确姿势'
    },
    {
        name: '悬垂举腿',
        aliases: [' hanging leg raise', '举腿'],
        category: 'core',
        equipment: ['单杠'],
        difficulty: 'advanced',
        steps: [
            '双手悬挂在单杠上',
            '举起双腿至与地面平行或更高',
            '缓慢下放'
        ],
        tips: [
            '控制晃动',
            '举得越高越难',
            '可以先从抬膝开始'
        ],
        commonErrors: [
            '晃动借力',
            '下放太快',
            '腿举不够高'
        ],
        videoSearchKeywords: '悬垂举腿教学'
    },
    {
        name: '俄罗斯转体',
        aliases: ['russian twist', '转体'],
        category: 'core',
        equipment: ['哑铃/药球'],
        difficulty: 'beginner',
        steps: [
            '坐姿，膝盖弯曲，脚可以离地或踩地',
            '身体后倾约45°',
            '双手持重物，左右转体',
            '触地或接近地面'
        ],
        tips: [
            '刺激腹斜肌',
            '脚离地更难',
            '转体时呼气'
        ],
        commonErrors: [
            '只动手不动躯干',
            '太快',
            '脚踩地太简单'
        ],
        videoSearchKeywords: '俄罗斯转体教学'
    },
    {
        name: '死虫',
        aliases: ['dead bug'],
        category: 'core',
        equipment: [],
        difficulty: 'beginner',
        steps: [
            '仰卧，双臂伸直指向天花板',
            '双腿抬起，膝盖弯曲90°',
            '对侧手脚同时向外伸展',
            '回到起始位置，换另一侧'
        ],
        tips: [
            '下背部始终贴地',
            '动作要慢',
            '保护腰椎的好动作'
        ],
        commonErrors: [
            '腰部拱起',
            '动作太快',
            '憋气'
        ],
        videoSearchKeywords: '死虫核心训练'
    },
    // 有氧/HIIT
    {
        name: '跑步',
        aliases: ['慢跑', 'running', 'jogging'],
        category: 'cardio',
        equipment: [],
        difficulty: 'beginner',
        steps: [
            '保持良好跑姿，身体微前倾',
            '前脚掌或中足着地',
            '手臂自然摆动',
            '保持呼吸节奏'
        ],
        tips: [
            '循序渐进增加距离',
            '穿合适的跑鞋',
            '注意跑姿'
        ],
        commonErrors: [
            '步幅过大',
            '脚后跟重着地',
            '过度前倾'
        ],
        videoSearchKeywords: '正确跑步姿势'
    },
    {
        name: '开合跳',
        aliases: ['jumping jack'],
        category: 'cardio',
        equipment: [],
        difficulty: 'beginner',
        steps: [
            '站立，双脚并拢，双手放在身体两侧',
            '跳起，双脚分开，双手举过头顶',
            '跳回起始位置',
            '重复'
        ],
        tips: [
            '热身好动作',
            '保持节奏',
            '膝盖微弯缓冲'
        ],
        commonErrors: [
            '落地太重',
            '动作不协调',
            '太快失去节奏'
        ],
        videoSearchKeywords: '开合跳正确姿势'
    },
    {
        name: '波比跳',
        aliases: ['burpee'],
        category: 'cardio',
        equipment: [],
        difficulty: 'intermediate',
        steps: [
            '站立，下蹲，双手撑地',
            '双脚向后跳成俯卧撑姿势',
            '做一个俯卧撑（可选）',
            '双脚跳回，向上跳起'
        ],
        tips: [
            '全身燃脂好动作',
            '保持节奏',
            '俯卧撑可以省略降低难度'
        ],
        commonErrors: [
            '动作不连贯',
            '核心松懈',
            '落地太重'
        ],
        videoSearchKeywords: '波比跳正确姿势'
    },
    {
        name: '登山跑',
        aliases: ['mountain climber'],
        category: 'cardio',
        equipment: [],
        difficulty: 'beginner',
        steps: [
            '俯卧撑姿势，双手撑地',
            '一只脚向胸前抬起',
            '快速交替双腿',
            '像在地上跑步'
        ],
        tips: [
            '核心始终收紧',
            '髋部不要抬太高',
            '可以慢速控制'
        ],
        commonErrors: [
            '塌腰',
            '臀部太高',
            '动作太快失去控制'
        ],
        videoSearchKeywords: '登山跑正确姿势'
    },
    {
        name: '深蹲跳',
        aliases: ['squat jump'],
        category: 'cardio',
        equipment: [],
        difficulty: 'intermediate',
        steps: [
            '深蹲姿势，大腿至少平行地面',
            '用力向上跳起',
            '落地回到深蹲姿势',
            '重复'
        ],
        tips: [
            '落地时膝盖缓冲',
            '落地直接进入下一个深蹲',
            '爆发力训练'
        ],
        commonErrors: [
            '落地太重',
            '深蹲不够深',
            '跳得不够高'
        ],
        videoSearchKeywords: '深蹲跳教学'
    },
    {
        name: '高抬腿',
        aliases: ['high knees'],
        category: 'cardio',
        equipment: [],
        difficulty: 'beginner',
        steps: [
            '原地跑步',
            '膝盖抬至髋部高度',
            '手臂配合摆动',
            '保持快节奏'
        ],
        tips: [
            '核心收紧',
            '前脚掌着地',
            '热身和心肺训练'
        ],
        commonErrors: [
            '腿抬得不够高',
            '落地太重',
            '身体过度后仰'
        ],
        videoSearchKeywords: '高抬腿正确姿势'
    }
];
/**
 * 根据动作名称查找详细讲解
 */
export function findExerciseDetail(name) {
    const lowerName = name.toLowerCase();
    return exerciseDetails.find(ex => ex.name === name ||
        ex.aliases.some(alias => alias.toLowerCase() === lowerName) ||
        lowerName.includes(ex.name.toLowerCase()) ||
        ex.name.toLowerCase().includes(lowerName));
}
/**
 * 获取动作的简要讲解（用于消息输出）
 */
export function getExerciseBrief(name) {
    const detail = findExerciseDetail(name);
    if (!detail)
        return '';
    return detail.tips[0] || detail.steps[0] || '';
}
/**
 * 获取动作的完整讲解
 */
export function getExerciseFullDescription(name) {
    const detail = findExerciseDetail(name);
    if (!detail)
        return `未找到 ${name} 的讲解`;
    const lines = [
        `📌 ${detail.name}`,
        '',
        '动作步骤：',
        ...detail.steps.map((s, i) => `${i + 1}. ${s}`),
        '',
        '要点：',
        ...detail.tips.map(t => `• ${t}`),
        '',
        '常见错误：',
        ...detail.commonErrors.map(e => `✗ ${e}`)
    ];
    return lines.join('\n');
}
