#!/usr/bin/env node
/**
 * Agent Manager - Gemini 风格界面
 * 支持图片输入、对话历史保存
 */

const express = require('express');
const cors = require('cors');
const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process');

const app = express();
const PORT = process.env.PORT || 3000;

const CONFIG = {
  agentsDir: path.join(process.env.HOME, '.openclaw/agents'),
  workspaceDir: path.join(process.env.HOME, '.openclaw')
};

app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

async function execCmd(cmd) {
  return new Promise((resolve, reject) => {
    exec(cmd, { shell: 'zsh' }, (error, stdout, stderr) => {
      if (error) reject(error);
      else resolve({ stdout, stderr });
    });
  });
}

async function readJsonFile(filepath) {
  const content = await fs.readFile(filepath, 'utf-8');
  return JSON.parse(content);
}

async function writeJsonFile(filepath, data) {
  await fs.mkdir(path.dirname(filepath), { recursive: true });
  await fs.writeFile(filepath, JSON.stringify(data, null, 2));
}

// API 路由
app.get('/api/agents', async (req, res) => {
  try {
    const agentsConfigPath = path.join(CONFIG.workspaceDir, 'agents.json');
    let registeredAgents = [];
    try {
      registeredAgents = await readJsonFile(agentsConfigPath);
    } catch (e) {}
    
    res.json({ success: true, registered: registeredAgents });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

app.post('/api/agents', async (req, res) => {
  try {
    const { name, description, model } = req.body;
    if (!name) return res.status(400).json({ success: false, error: '名称必填' });
    
    const agentId = `agent-${name.toLowerCase().replace(/\s+/g, '-')}`;
    const agentDir = path.join(CONFIG.agentsDir, agentId);
    await fs.mkdir(agentDir, { recursive: true });
    
    const agentConfig = {
      id: agentId,
      name,
      description: description || '',
      model: model || 'bailian/qwen3.5-plus',
      workspace: `workspace-${name.toLowerCase()}`,
      createdAt: new Date().toISOString(),
      status: 'active'
    };
    
    await writeJsonFile(path.join(agentDir, 'config.json'), agentConfig);
    await fs.writeFile(path.join(agentDir, 'IDENTITY.md'), `# ${name}\n\n- **Name:** ${name}\n- **Role:** Agent\n`);
    await fs.writeFile(path.join(agentDir, 'SOUL.md'), `# ${name}\n\n_做最好的自己_\n`);
    
    const agentsConfigPath = path.join(CONFIG.workspaceDir, 'agents.json');
    let allAgents = [];
    try { allAgents = await readJsonFile(agentsConfigPath); } catch (e) {}
    allAgents.push(agentConfig);
    await writeJsonFile(agentsConfigPath, allAgents);
    
    res.json({ success: true, agent: agentConfig, message: `Agent "${name}" 创建成功！` });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

app.post('/api/agents/:id/chat', async (req, res) => {
  try {
    const { id } = req.params;
    const { message, imageData } = req.body;
    
    if (!message && !imageData) {
      return res.status(400).json({ success: false, error: '消息或图片不能为空' });
    }
    
    const agentId = id.replace('agent-', '');
    const workspace = `workspace-${agentId}`;
    const workspacePath = path.join(CONFIG.workspaceDir, workspace);
    
    try { await fs.access(workspacePath); } catch (e) {
      return res.status(404).json({ success: false, error: `Agent 工作区不存在：${workspace}` });
    }
    
    let taskMessage = message || '请分析这张图片';
    if (imageData) {
      taskMessage = `${message || ''} [图片已上传]`.trim();
    }
    
    const safeMessage = taskMessage.replace(/"/g, '\\"').replace(/\n/g, ' ');
    const { stdout } = await execCmd(`cd "${workspacePath}" && openclaw agent --agent ${agentId} --message "${safeMessage}" --json 2>&1`);
    
    let cleanResponse = stdout;
    try {
      const jsonStart = stdout.indexOf('{');
      if (jsonStart !== -1) {
        const jsonStr = stdout.substring(jsonStart);
        const result = JSON.parse(jsonStr);
        if (result.result?.payloads?.[0]?.text) {
          cleanResponse = result.result.payloads[0].text;
        }
      }
    } catch (e) {}
    
    res.json({
      success: true,
      response: cleanResponse,
      agent: id,
      workspace: workspace,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

app.delete('/api/agents/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const agentDir = path.join(CONFIG.agentsDir, id);
    try { await fs.access(agentDir); } catch (e) {
      return res.status(404).json({ success: false, error: 'Agent 不存在' });
    }
    await execCmd(`rm -rf "${agentDir}"`);
    
    const agentsConfigPath = path.join(CONFIG.workspaceDir, 'agents.json');
    let allAgents = [];
    try { allAgents = await readJsonFile(agentsConfigPath); } catch (e) {
      return res.json({ success: true, message: '已删除' });
    }
    allAgents = allAgents.filter(a => a.id !== id);
    await writeJsonFile(agentsConfigPath, allAgents);
    
    res.json({ success: true, message: `Agent "${id}" 已删除` });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Gemini 风格界面 - 使用独立 HTML 文件
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// 备用：内嵌 HTML（如果文件不存在）
app.get('/embedded', (req, res) => {
  res.send(`<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Agent Manager</title>
  <style>
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#fff;height:100vh;overflow:hidden}
    .main-container{display:flex;height:100vh}
    .sidebar{width:280px;background:#f0f4f9;border-right:1px solid #e0e0e0;display:flex;flex-direction:column}
    .sidebar-header{padding:20px;border-bottom:1px solid #e0e0e0}
    .sidebar-header h2{font-size:18px;color:#1a1a1a;margin-bottom:15px;font-weight:500}
    .add-agent-btn{width:100%;background:#fff;color:#1a73e8;border:1px solid #dadce0;padding:12px;border-radius:8px;cursor:pointer;font-size:14px;font-weight:500}
    .add-agent-btn:hover{background:#f8f9fa}
    .agent-list{flex:1;overflow-y:auto;padding:12px}
    .agent-item{padding:14px 16px;margin-bottom:8px;background:#fff;border:2px solid transparent;border-radius:12px;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.05)}
    .agent-item:hover{border-color:#1a73e8;box-shadow:0 2px 8px rgba(26,115,232,0.15)}
    .agent-item.active{border-color:#1a73e8;background:#e8f0fe}
    .agent-name{font-weight:500;color:#1a1a1a;font-size:15px;display:flex;align-items:center}
    .agent-emoji{font-size:18px;margin-right:10px}
    .agent-desc{color:#5f6368;font-size:12px;margin-top:6px}
    .chat-area{flex:1;display:flex;flex-direction:column;background:#fff}
    .chat-header{padding:16px 24px;border-bottom:1px solid #e0e0e0}
    .chat-header-content{display:flex;align-items:center;justify-content:space-between}
    .chat-header h2{font-size:20px;color:#1a1a1a;display:flex;align-items:center;font-weight:500}
    .agent-status{background:#e8f0fe;color:#1a73e8;padding:4px 12px;border-radius:12px;font-size:12px;display:flex;align-items:center;gap:6px}
    .agent-status::before{content:'';width:6px;height:6px;background:#1a73e8;border-radius:50%}
    .chat-messages{flex:1;overflow-y:auto;padding:40px 60px;display:flex;flex-direction:column;gap:24px;background:#fff}
    .message{max-width:85%;padding:18px 22px;border-radius:18px;animation:fadeIn 0.3s;box-shadow:0 1px 3px rgba(0,0,0,0.08)}
    @keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
    .message.user{align-self:flex-end;background:#1a73e8;color:white;border-bottom-right-radius:4px}
    .message.agent{align-self:flex-start;background:#f0f4f9;color:#1a1a1a;border:1px solid #e0e0e0;border-bottom-left-radius:4px}
    .message-content{font-size:15px;white-space:pre-wrap;line-height:1.6}
    .message-image{max-width:100%;max-height:300px;border-radius:8px;margin-top:10px;display:block}
    .message-header{font-size:12px;margin-bottom:6px;opacity:0.8;font-weight:500}
    .message-time{font-size:11px;margin-top:8px;opacity:0.6;text-align:right}
    .empty-state{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#5f6368}
    .empty-state-icon{font-size:96px;margin-bottom:32px;opacity:0.3}
    .empty-state-text{font-size:20px;text-align:center;color:#1a1a1a}
    .empty-state-subtext{font-size:15px;color:#5f6368;margin-top:16px}
    .chat-input-area{padding:24px 60px 32px;border-top:1px solid #e0e0e0;background:#fff}
    .input-wrapper{background:#f0f4f9;border-radius:28px;padding:16px 20px;display:flex;align-items:flex-end;gap:12px;border:2px solid transparent;transition:all 0.2s;box-shadow:0 1px 3px rgba(0,0,0,0.05)}
    .input-wrapper:focus-within{background:#fff;border-color:#1a73e8;box-shadow:0 2px 12px rgba(26,115,232,0.15)}
    .chat-input{flex:1;padding:14px 16px;border:none;background:transparent;font-size:16px;outline:none;resize:none;max-height:300px;font-family:inherit;line-height:1.5;min-height:24px}
    .chat-input::placeholder{color:#9aa0a6}
    .image-preview-container{display:flex;gap:12px;padding:0 20px 16px;flex-wrap:wrap}
    .image-preview{position:relative;width:100px;height:100px;border-radius:12px;overflow:hidden;border:2px solid #1a73e8;box-shadow:0 2px 8px rgba(26,115,232,0.2)}
    .image-preview img{width:100%;height:100%;object-fit:cover}
    .image-preview .remove-btn{position:absolute;top:4px;right:4px;width:20px;height:20px;background:#f44336;color:white;border:none;border-radius:50%;cursor:pointer;font-size:12px;display:flex;align-items:center;justify-content:center}
    .input-actions{display:flex;gap:8px;align-items:center}
    .attach-btn{width:48px;height:48px;border-radius:50%;border:none;background:#fff;color:#5f6368;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:20px;box-shadow:0 2px 6px rgba(0,0,0,0.1);transition:all 0.2s}
    .attach-btn:hover{background:#1a73e8;color:white;transform:scale(1.1)}
    .send-btn{background:#1a73e8;color:white;border:none;width:52px;height:52px;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:20px;transition:all 0.2s;box-shadow:0 2px 8px rgba(26,115,232,0.3)}
    .send-btn:hover{transform:scale(1.05);box-shadow:0 2px 8px rgba(26,115,232,0.3)}
    .send-btn:disabled{opacity:0.4;cursor:not-allowed;transform:none}
    .modal-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);display:none;align-items:center;justify-content:center;z-index:1000}
    .modal-overlay.active{display:flex}
    .modal{background:white;border-radius:16px;width:480px;max-width:90%;padding:32px;box-shadow:0 20px 60px rgba(0,0,0,0.3)}
    .modal h2{margin-bottom:24px;color:#1a1a1a;font-size:20px;font-weight:500}
    .modal-form .form-group{margin-bottom:20px}
    .modal-form label{display:block;margin-bottom:8px;font-weight:500;color:#5f6368;font-size:14px}
    .modal-form input,.modal-form textarea,.modal-form select{width:100%;padding:14px 16px;border:2px solid #e0e0e0;border-radius:10px;font-size:15px;outline:none}
    .modal-form input:focus,.modal-form textarea:focus,.modal-form select:focus{border-color:#1a73e8}
    .modal-form textarea{resize:vertical;min-height:90px;font-family:inherit}
    .modal-actions{display:flex;gap:12px;margin-top:28px}
    .modal-actions button{flex:1;padding:14px;border:none;border-radius:10px;cursor:pointer;font-size:15px;font-weight:500}
    .modal-actions .cancel-btn{background:#f0f4f9;color:#5f6368}
    .modal-actions .submit-btn{background:#1a73e8;color:white}
    .loading{display:flex;align-items:center;gap:10px;color:#5f6368;padding:20px}
    .loading-spinner{width:18px;height:18px;border:2px solid #e0e0e0;border-top-color:#1a73e8;border-radius:50%;animation:spin 1s linear infinite}
    @keyframes spin{to{transform:rotate(360deg)}}
    #fileInput{display:none}
    .clear-history-btn{padding:8px 16px;font-size:13px;background:#f44336;color:white;border:none;border-radius:8px;cursor:pointer}
    .clear-history-btn:hover{background:#d32f2f}
  </style>
</head>
<body>
  <div class="main-container">
    <div class="sidebar">
      <div class="sidebar-header">
        <h2>Agent Manager</h2>
        <button class="add-agent-btn" onclick="showAddModal()">+ 新建 Agent</button>
      </div>
      <div class="agent-list" id="agentList"><div class="loading"><div class="loading-spinner"></div>加载中...</div></div>
    </div>
    <div class="chat-area">
      <div class="chat-header" id="chatHeader" style="display:none">
        <div class="chat-header-content">
          <h2><span class="agent-emoji">🤖</span><span id="chatAgentName">选择 Agent</span></h2>
          <div style="display:flex;gap:10px;align-items:center">
            <span class="agent-status">在线</span>
            <button onclick="clearCurrentHistory()" class="clear-history-btn">清空历史</button>
          </div>
        </div>
      </div>
      <div class="chat-messages" id="chatMessages">
        <div class="empty-state">
          <div class="empty-state-icon">💬</div>
          <div class="empty-state-text">选择一个 Agent 开始对话</div>
          <div class="empty-state-subtext">💡 支持文字、图片输入，可直接拖拽图片到输入框</div>
        </div>
      </div>
      <div class="chat-input-area" id="chatInputArea" style="display:none">
        <div class="image-preview-container" id="imagePreview"></div>
        <div class="input-wrapper">
          <textarea class="chat-input" id="chatInput" placeholder="输入消息，或点击 📎 上传图片（支持拖拽）..." rows="1" onkeydown="autoResize(this)" onkeypress="handleKeyPress(event)" ondrop="handleDrop(event)" ondragover="handleDragOver(event)"></textarea>
          <div class="input-actions">
            <input type="file" id="fileInput" accept="image/*" multiple onchange="handleFileSelect(event)">
            <button class="attach-btn" onclick="document.getElementById('fileInput').click()" title="上传图片">📎</button>
            <button class="send-btn" id="sendBtn" onclick="sendMessage()">➤</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-overlay" id="addModal">
    <div class="modal">
      <h2>创建新 Agent</h2>
      <form class="modal-form" id="addAgentForm">
        <div class="form-group"><label>名称 *</label><input type="text" id="agentName" placeholder="如：Judy, MNK, Fly" required></div>
        <div class="form-group"><label>描述</label><textarea id="agentDesc" rows="3" placeholder="Agent 的职责描述"></textarea></div>
        <div class="form-group"><label>模型</label><select id="agentModel"><option value="bailian/qwen3.5-plus">通义千问 3.5 Plus</option><option value="bailian/glm-5">智谱 GLM-5</option></select></div>
        <div class="modal-actions">
          <button type="button" class="cancel-btn" onclick="hideAddModal()">取消</button>
          <button type="submit" class="submit-btn">创建 Agent</button>
        </div>
      </form>
    </div>
  </div>
  <script>
    const API_BASE='/api',STORAGE_KEY='agent_manager_chat_history';
    let currentAgentId=null,agents=[],chatHistory={},selectedImages=[];
    const agentEmojis={judy:'💼',mnk:'🦾',fly:'🕊️',dav:'📊',zhou:'📈',pnews:'📰'};
    
    function loadChatHistory(){try{const s=localStorage.getItem(STORAGE_KEY);if(s)chatHistory=JSON.parse(s)}catch(e){chatHistory={}}}
    function saveChatHistory(){try{localStorage.setItem(STORAGE_KEY,JSON.stringify(chatHistory))}catch(e){}}
    function getAgentHistory(id){return chatHistory[id]||[]}
    function addMessageToHistory(id,msg){if(!chatHistory[id])chatHistory[id]=[];chatHistory[id].push(msg);if(chatHistory[id].length>100)chatHistory[id]=chatHistory[id].slice(-100);saveChatHistory()}
    function clearCurrentHistory(){if(!currentAgentId)return;if(confirm('确定清空对话历史？')){chatHistory[currentAgentId]=[];saveChatHistory();selectAgent(currentAgentId)}}
    function autoResize(t){t.style.height='auto';t.style.height=Math.min(t.scrollHeight,200)+'px'}
    function handleFileSelect(e){for(let f of e.target.files){if(f.type.startsWith('image/')){const r=new FileReader();r.onload=(ev)=>{selectedImages.push({name:f.name,data:ev.target.result});renderImagePreviews()};r.readAsDataURL(f)}}e.target.value=''}
    function renderImagePreviews(){const c=document.getElementById('imagePreview');if(selectedImages.length===0){c.innerHTML='';return}c.innerHTML=selectedImages.map((img,i)=>'<div class="image-preview"><img src="'+img.data+'"><button class="remove-btn" onclick="removeImage('+i+')">×</button></div>').join('')}
    function removeImage(i){selectedImages.splice(i,1);renderImagePreviews()}
    function clearSelectedImages(){selectedImages=[];renderImagePreviews()}
    function handleDragOver(e){e.preventDefault();e.stopPropagation()}
    function handleDrop(e){e.preventDefault();e.stopPropagation();const files=e.dataTransfer.files;for(let f of files){if(f.type.startsWith('image/')){const r=new FileReader();r.onload=(ev)=>{selectedImages.push({name:f.name,data:ev.target.result});renderImagePreviews()};r.readAsDataURL(f)}}}
    
    async function loadAgents(){try{const r=await fetch(API_BASE+'/agents'),d=await r.json();agents=d.registered||[];if(agents.length===0){document.getElementById('agentList').innerHTML='<div style="padding:20px;color:#666;text-align:center">暂无 Agent</div>';return}document.getElementById('agentList').innerHTML=agents.map(a=>{const emoji=agentEmojis[a.id.replace('agent-','')]||'🤖',active=a.id===currentAgentId?'active':'';return '<div class="agent-item '+active+'" onclick="selectAgent(\''+a.id+'\')"><div class="agent-name"><span class="agent-emoji">'+emoji+'</span>'+a.name+'</div><div class="agent-desc">'+(a.description||'')+'</div></div>'}).join('')}catch(e){document.getElementById('agentList').innerHTML='<div style="padding:20px;color:#f44336">加载失败</div>'}}
    
    function selectAgent(agentId){currentAgentId=agentId;const agent=agents.find(a=>a.id===agentId);document.querySelectorAll('.agent-item').forEach(i=>i.classList.remove('active'));if(event&&event.currentTarget)event.currentTarget.classList.add('active');document.getElementById('chatHeader').style.display='block';document.getElementById('chatInputArea').style.display='block';const emoji=agentEmojis[agentId.replace('agent-','')]||'🤖';document.getElementById('chatAgentName').textContent=agent.name;document.querySelector('#chatHeader .agent-emoji').textContent=emoji;const history=getAgentHistory(agentId),chatMessages=document.getElementById('chatMessages');if(history.length===0){chatMessages.innerHTML='<div class="empty-state"><div class="empty-state-icon">'+emoji+'</div><div class="empty-state-text">开始与 '+agent.name+' 对话</div></div>'}else{chatMessages.innerHTML=history.map(m=>{const imgHtml=m.image?'<img src="'+m.image+'" class="message-image">':'';return '<div class="message '+m.type+'"><div class="message-header">'+(m.type==='user'?'你':emoji+' '+agent.name)+'</div><div class="message-content">'+escapeHtml(m.content)+'</div>'+imgHtml+'<div class="message-time">'+m.time+'</div></div>'}).join('');chatMessages.scrollTop=chatMessages.scrollHeight}}
    
    async function sendMessage(){const input=document.getElementById('chatInput'),message=input.value.trim();if(!currentAgentId||(!message&&selectedImages.length===0))return;const agent=agents.find(a=>a.id===currentAgentId),emoji=agentEmojis[currentAgentId.replace('agent-','')]||'🤖',time=new Date().toLocaleTimeString('zh-CN',{hour:'2-digit',minute:'2-digit'}),chatMessages=document.getElementById('chatMessages');let imageData=null;if(selectedImages.length>0){imageData=selectedImages[0].data}addMessageToHistory(currentAgentId,{type:'user',content:message,image:imageData,time:time});const history=getAgentHistory(currentAgentId);if(history.length===1)chatMessages.innerHTML='';const imgPreview=imageData?'<img src="'+imageData+'" class="message-image">':'';chatMessages.innerHTML+='<div class="message user"><div class="message-header">你</div><div class="message-content">'+escapeHtml(message)+(imageData?' [图片]':'')+'</div>'+imgPreview+'<div class="message-time">'+time+'</div></div>';input.value='';clearSelectedImages();chatMessages.scrollTop=chatMessages.scrollHeight;const sendBtn=document.getElementById('sendBtn');sendBtn.disabled=true;try{const r=await fetch(API_BASE+'/agents/'+currentAgentId+'/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message,imageData})}),d=await r.json();if(d.success){addMessageToHistory(currentAgentId,{type:'agent',content:d.response,time:time});chatMessages.innerHTML+='<div class="message agent"><div class="message-header">'+emoji+' '+agent.name+'</div><div class="message-content">'+escapeHtml(d.response)+'</div><div class="message-time">'+time+'</div></div>'}else{chatMessages.innerHTML+='<div class="message agent" style="background:#ffe6e6;border-color:#f44336"><div class="message-content">❌ 错误：'+escapeHtml(d.error)+'</div></div>'}}catch(e){chatMessages.innerHTML+='<div class="message agent" style="background:#ffe6e6;border-color:#f44336"><div class="message-content">❌ 请求失败：'+escapeHtml(e.message)+'</div></div>'}sendBtn.disabled=false;chatMessages.scrollTop=chatMessages.scrollHeight}
    
    function handleKeyPress(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMessage()}}
    function showAddModal(){document.getElementById('addModal').classList.add('active')}
    function hideAddModal(){document.getElementById('addModal').classList.remove('active');document.getElementById('addAgentForm').reset()}
    document.getElementById('addAgentForm').addEventListener('submit',async(e)=>{e.preventDefault();const name=document.getElementById('agentName').value,description=document.getElementById('agentDesc').value,model=document.getElementById('agentModel').value;try{const r=await fetch(API_BASE+'/agents',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,description,model})}),d=await r.json();if(d.success){alert('创建成功！');hideAddModal();loadAgents()}else{alert('创建失败：'+d.error)}}catch(e){alert('创建失败：'+e.message)}});
    function escapeHtml(t){const d=document.createElement('div');d.textContent=t;return d.innerHTML}
    loadChatHistory();loadAgents();
  </script>
</body>
</html>`);
});

app.listen(PORT, () => {
  console.log(`🚀 Agent Manager 运行在 http://localhost:${PORT}`);
});
