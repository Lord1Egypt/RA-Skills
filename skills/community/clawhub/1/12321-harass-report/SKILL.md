---
name: 12321-harass-report
description: |
  12321网络不良与垃圾信息举报受理中心 - 骚扰电话举报自动化。
  当用户说"举报骚扰电话"、"12321举报"、"投诉骚扰电话"、"填写举报表单"、"打开12321"时触发。
  支持完整的交互式举报流程：绕过倒计时→验证码识别→信息确认→短信验证码→填表→校验→提交。
---

# 12321 骚扰电话举报

自动化填写 12321 骚扰电话举报表单，通过浏览器交互+聊天确认完成举报。

## 完整流程（两步交互）

### 阶段1: 打开页面 + 绕过倒计时

1. 浏览器打开 `https://www.12321.cn/notifyHomePhone`
2. JS evaluate：

```js
if(typeof counts!=='undefined')counts=0;
if(typeof counting!=='undefined')clearInterval(counting);
const btn=document.getElementById('btnAgree');
if(btn){btn.disabled=false;btn.textContent='我同意';btn.click();}
```

### 阶段2: 验证码提取 + OCR + 发送图片 + 一次性确认全部信息

**步骤1：提取验证码 base64**
```js
const c=document.createElement('canvas');
const img=document.getElementById('code');
c.width=img.naturalWidth; c.height=img.naturalHeight;
c.getContext('2d').drawImage(img,0,0);
return c.toDataURL('image/png');
```

**步骤2：保存为 PNG 文件**

⚠️ PowerShell 直接赋值 base64 长字符串会因截断/特殊字符失败。用 node 方式：
```
1. 将 base64 字符串（去掉 data:image/png;base64, 前缀）写入 captcha.txt
2. node -e "const fs=require('fs');const b=fs.readFileSync('captcha.txt','utf8').trim();fs.writeFileSync('captcha.png',Buffer.from(b,'base64'));"
```

**步骤3：OCR 识别**
```
image(prompt='Read all characters in the captcha image', image='captcha.png')
```
如果失败，备用：直接用 URL 做 OCR
```
image(prompt='Read all characters in the captcha image', image='https://www.12321.cn/Com-code.html')
```

**步骤4：发送验证码图片给用户**
```
message(action='send', filePath='captcha.png', message='验证码识别：{ocr}（与图片不一致请回复正确的）\n\n📋 举报信息...')
```

⚠️ **必须同时发送验证码图片文件（filePath）和确认消息**，让用户可以核对 OCR 是否正确。

**确认消息模板：**
```
验证码识别：{ocr}（与图片不一致请回复正确的）

📋 举报信息（默认值如下，需修改请指出对应编号）：

1️⃣ 验证码：{ocr}
2️⃣ 您的手机号：13585916639
3️⃣ 举报号码：{用户消息中提取，去空格}
4️⃣ 骚扰时间：{today} {now}
5️⃣ 通话时长：3分钟以下
6️⃣ 骚扰方式：自动语音骚扰
7️⃣ 不良类型：⑦贷款理财
    ①淫秽色情 ②虚假票证 ③反动谣言 ④房产中介 ⑤保险推销 ⑥教育培训 ⑦贷款理财 ⑧猎头招聘 ⑨欠款催收 ⑩医疗保健 ⑪股票证券 ⑫旅游推广 ⑬食药推销 ⑭POS机推销 ⑮装修建材 ⑯网络游戏 ⑰App推广 ⑱出行拉货 ⑲零售业推销 ⑳电信业务推广 ㉑其他营销
8️⃣ 来电描述：近期未经过我的授权，不同的机构、不同的人员给我拨打推销电话、骚扰电话。

全部确认回复"确认"，修改请回复如"7→⑤"或"6→人工骚扰"。
```

**默认值：**
| 字段 | 默认值 |
|------|--------|
| 手机号 | 历史最后一个（优先 13585916639） |
| 举报号码 | 用户消息提取，去空格 |
| 日期/时间 | 今日/当前 |
| 通话时长 | 3分钟以下(0) |
| 骚扰方式 | 自动语音骚扰(1) |
| 不良类型 | 贷款理财(7) |
| 来电描述 | 近期未经过我的授权，不同的机构、不同的人员给我拨打推销电话、骚扰电话。 |

**等待用户回复。**

### 阶段2.5: 用户修改信息（不刷新页面）

用户修改信息时只记录新值，**不等同于确认**。修改后发送更新确认消息，等待用户说"确认"。

### 阶段3: 填入验证码+手机号 → 验证 → 触发短信

⚠️ **核心：全部在同一次 evaluate 中完成！Validform 会在 evaluate 返回后清空 w_code。**

⚠️ **w_code 必须用 `el.value=` 直接赋值（不用 nativeInputValueSetter），且必须触发 `input` 事件让 Validform 感知值变化。**

```js
() => {
  // 1. 填入验证码
  const el=document.getElementById('w_code');
  el.removeAttribute('onkeyup');
  el.removeAttribute('onpaste');
  el.removeAttribute('oncontextmenu');
  el.value='{captcha}';
  el.dispatchEvent(new Event('input',{bubbles:true}));

  // 2. 验证值
  const w=el.value;
  if(!w){return JSON.stringify({error:'验证码为空，请刷新页面重试'});}

  // 3. 填入手机号
  const s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
  const el2=document.getElementById('phone');
  s.call(el2,'{phone}');
  el2.dispatchEvent(new Event('input',{bubbles:true}));
  el2.blur();

  // 4. 触发短信
  document.getElementById('hq2').click();

  return JSON.stringify({
    w:document.getElementById('w_code').value,
    p:document.getElementById('phone').value,
    t:document.getElementById('Time')?.textContent?.trim()
  });
}
```

**检查返回值：**
- `error` → 刷新页面重来
- `w` 非空 + `t` 显示"重新获取(59)" → 成功

**发送确认消息后等待短信验证码。**

### 阶段4: 填写剩余字段（分3次 evaluate）

**第1次：短信验证码 + 举报号码**
```js
const s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
const pc=document.getElementById('p_code');
pc.focus(); s.call(pc,'{sms_code}');
pc.dispatchEvent(new Event('input',{bubbles:true}));
pc.dispatchEvent(new Event('change',{bubbles:true})); pc.blur();
const sp=document.getElementById('sms_phone');
sp.focus(); s.call(sp,'{report_phone}');
sp.dispatchEvent(new Event('input',{bubbles:true}));
sp.dispatchEvent(new Event('change',{bubbles:true})); sp.blur();
return JSON.stringify({p_code:pc.value, sms_phone:sp.value});
```

**第2次：日期时间 + 通话时长 + 骚扰方式 + 不良类型**
```js
const fire=(el)=>{
  ['focus','input','change','blur'].forEach(e=>el.dispatchEvent(new Event(e,{bubbles:true})));
};
document.getElementById('d241').value='{YYYY-MM-DD}';
fire(document.getElementById('d241'));
document.getElementById('d241').click();
document.getElementById('d242').value='{HH:mm}';
fire(document.getElementById('d242'));
document.getElementById('d242').click();
document.getElementById('d243').value='{long_time}';
fire(document.getElementById('d243'));
document.querySelectorAll('input[name="type"]').forEach(r=>{
  if(r.value==='{type}'){r.checked=true;r.dispatchEvent(new Event('change',{bubbles:true}));}
});
document.querySelectorAll('input[name="bad_type"]').forEach(r=>{
  if(r.value==='{bad_type}'){r.checked=true;r.dispatchEvent(new Event('change',{bubbles:true}));}
});
return 'radios done';
```

**第3次：来电描述 + 勾选同意**
```js
const ts=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set;
const sc=document.getElementById('sms_content');
ts.call(sc,'{来电描述}');
sc.dispatchEvent(new Event('input',{bubbles:true}));
sc.dispatchEvent(new Event('change',{bubbles:true}));
sc.blur();
const flag=document.getElementById('user_intention_flag');
if(flag&&!flag.checked)flag.click();
return 'desc+flag done';
```

### 阶段5: 校验 + 确认提交

```js
const errs=[];
document.querySelectorAll('#sc_xg_2,#sc_xg_1,.Validform_wrong,.Validform_error')
  .forEach(el=>{if(el.style.display!=='none'&&el.textContent.trim())errs.push(el.id+':'+el.textContent.trim());});
const vals={w_code:document.getElementById('w_code').value,
  phone:document.getElementById('phone').value,
  p_code:document.getElementById('p_code').value,
  sms_phone:document.getElementById('sms_phone').value,
  d241:document.getElementById('d241').value, d242:document.getElementById('d242').value,
  type:document.querySelector('input[name=type]:checked')?.value,
  bad_type:document.querySelector('input[name=bad_type]:checked')?.value,
  sms_content:document.getElementById('sms_content').value,
  xuzhi:document.getElementById('xuzhi').checked};
return JSON.stringify({vals,errs});
```

- `errs` 为空 → 校验通过，确认是否提交
- `#sc_ts`（"请填写来电的内容"）是页面初始提示，可忽略
- 有错误 → 告知用户并修正

### 阶段6: 提交

⚠️ 提交按钮是 **`#sub_jb`**（不是 `btnSubmit`）。

```js
document.getElementById('sub_jb').click();
```

提交后检查页面是否跳转：
```js
return JSON.stringify({url:location.href, success:!!document.body?.innerText?.match(/成功|感谢|已受理/)});
```

- 页面跳转/显示成功 → 举报完成，关闭浏览器标签页
- 仍在表单页 → 检查错误提示，可能是短信验证码过期，需重新获取

### 阶段7: 关闭浏览器

举报完成（成功或用户放弃）后，关闭浏览器标签页：
```
browser(action='close', targetId='{当前targetId}')
```

## 字段映射

详见 [references/field-mapping.md](references/field-mapping.md)

## 实测踩坑记录

### w_code 验证码填入（最核心）

| 方式 | 结果 | 原因 |
|------|------|------|
| nativeInputValueSetter + input | ❌ 被清空 | Validform 拦截 setter |
| el.value= 不触发事件 | ❌ 后端不认 | Validform 没感知值变化 |
| **el.value= + input事件** | ✅ 成功 | 赋值不被拦截，事件触发校验 |
| 分两次 evaluate | ❌ 被清空 | Validform 在 evaluate 返回后清空 |

**结论：`el.value=` + `dispatchEvent('input')` + `hq2.click()` 必须在同一次 evaluate 中。**

### 其他字段
- textarea 用 `HTMLTextAreaElement.prototype` setter（不是 HTMLInputElement 的）
- 日期/时间 readonly，赋值后需 `.click()` 触发控件校验
- base64 中的 `+` 在 PowerShell 中需用单引号变量包裹
- **验证码图片保存方式**：PowerShell 赋值长 base64 会截断，必须用 node 读 txt 写 png
- **必须发送验证码图片给用户确认**：用 `message(filePath='captcha.png')` 发送图片

## 不良类型选项

①淫秽色情 ②虚假票证 ③反动谣言 ④房产中介 ⑤保险推销 ⑥教育培训 ⑦贷款理财 ⑧猎头招聘 ⑨欠款催收 ⑩医疗保健 ⑪股票证券 ⑫旅游推广 ⑬食药推销 ⑭POS机推销 ⑮装修建材 ⑯网络游戏 ⑰App推广 ⑱出行拉货 ⑲零售业推销 ⑳电信业务推广 ㉑其他营销
