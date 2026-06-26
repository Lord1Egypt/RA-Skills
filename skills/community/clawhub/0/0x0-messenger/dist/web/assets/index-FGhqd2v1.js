(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const d of document.querySelectorAll('link[rel="modulepreload"]'))a(d);new MutationObserver(d=>{for(const s of d)if(s.type==="childList")for(const o of s.addedNodes)o.tagName==="LINK"&&o.rel==="modulepreload"&&a(o)}).observe(document,{childList:!0,subtree:!0});function i(d){const s={};return d.integrity&&(s.integrity=d.integrity),d.referrerPolicy&&(s.referrerPolicy=d.referrerPolicy),d.crossOrigin==="use-credentials"?s.credentials="include":d.crossOrigin==="anonymous"?s.credentials="omit":s.credentials="same-origin",s}function a(d){if(d.ep)return;d.ep=!0;const s=i(d);fetch(d.href,s)}})();class ${constructor(){this.ws=null,this.handlers=new Map,this.reconnectTimer=null}connect(){this.ws=new WebSocket(`ws://localhost:${location.port||3e3}`),this.ws.onmessage=t=>{try{const i=JSON.parse(t.data);(this.handlers.get(i.event)||[]).forEach(d=>d(i))}catch{}},this.ws.onclose=()=>{this.reconnectTimer=setTimeout(()=>this.connect(),2e3)},this.ws.onerror=()=>{this.ws?.close()}}on(t,i){this.handlers.has(t)||this.handlers.set(t,[]),this.handlers.get(t).push(i)}send(t,i={}){this.ws?.readyState===WebSocket.OPEN&&this.ws.send(JSON.stringify({cmd:t,...i}))}destroy(){this.reconnectTimer&&clearTimeout(this.reconnectTimer),this.ws?.close()}}const l=new $,e={number:"",inbox:[],contacts:[],activePin:null,activeContact:null,messages:{},contactMessages:{},peerStatus:{},theme:"dark",screen:"welcome",newPinValue:b(),lobbyThreads:{},activeLobbyKey:null,newPinExpiry:"none",newPinCustomNum:"6",newPinCustomUnit:"h",newPinIsLobby:!1};function b(){return Math.floor(Math.random()*65536).toString(16).padStart(4,"0")}function c(){const n=document.getElementById("app");n.innerHTML=L(),_()}function L(){return`
    <div class="topbar">
      <span class="topbar-logo">0x0</span>
      <button class="theme-toggle" id="theme-toggle">
        // ${e.theme==="dark"?"dark":"light"}
      </button>
    </div>
    <div class="main-area">
      ${k()}
      <div class="panel ${e.screen!=="welcome"?"active":""}">
        ${B()}
      </div>
    </div>
  `}function k(){const n=e.inbox.filter(a=>a.type==="lobby"),t=e.inbox.filter(a=>a.type!=="lobby"),i=e.contacts;return`
    <div class="sidebar">
      <div class="number-section">
        <div class="section-label">// my_number</div>
        <div class="my-number" id="my-number">${e.number||"..."}</div>
        <div class="number-actions">
          <button class="pill-btn" id="btn-copy">// COPY</button>
          <button class="pill-btn" id="btn-renew">// RENEW</button>
        </div>
      </div>
      ${n.length>0?`
      <div class="inbox-section">
        <div style="padding: 12px 20px 6px">
          <div class="section-label">// requests</div>
        </div>
        ${n.map(a=>C(a)).join("")}
      </div>
      `:""}
      <div class="inbox-section">
        <div style="padding: 12px 20px 6px">
          <div class="section-label">// inbox</div>
        </div>
        ${t.map(a=>N(a)).join("")}
      </div>
      <button class="new-pin-btn" id="btn-new-pin">+ // NEW_PIN</button>
      <div class="contacts-section">
        <div style="padding: 12px 20px 6px; display:flex; justify-content:space-between; align-items:center">
          <div class="section-label">// contacts</div>
          <button class="pill-btn" id="btn-connect">+ CONNECT</button>
        </div>
        ${i.length===0?'<div style="padding:8px 20px; font-size:11px; opacity:0.4">// no contacts yet</div>':i.map(a=>q(a)).join("")}
      </div>
    </div>
  `}function C(n){const t=e.activePin?.id===n.id&&(e.screen==="requests"||e.screen==="requestChat"),i=e.lobbyThreads[n.id]||[],a=i.length,d=i.reduce((o,u)=>o+u.count,0),s=a>0?`${a} 件の差出人`:"(待機中)";return`
    <div class="inbox-item ${t?"active":""}" data-pin-id="${n.id}">
      <div class="peer-dot"></div>
      <div class="inbox-pin">${r(n.value)}</div>
      <div class="inbox-info">
        <div class="inbox-label">${r(n.label||"(公開用)")}</div>
        <div class="inbox-preview">${r(s)}</div>
      </div>
      <div class="inbox-meta">
        <div class="inbox-badge" data-count="${d}">${d||""}</div>
      </div>
    </div>
  `}function N(n){const t=e.activePin?.id===n.id&&e.screen==="chat",i=e.peerStatus[n.id]||"disconnected",a=n.latest?I(n.latest.timestamp):"",d=n.latest?n.latest.content.slice(0,35)+(n.latest.content.length>35?"…":""):"(no messages)";return`
    <div class="inbox-item ${t?"active":""}" data-pin-id="${n.id}">
      <div class="peer-dot ${i==="connected"?"connected":""}"></div>
      <div class="inbox-pin">${r(n.value)}</div>
      <div class="inbox-info">
        <div class="inbox-label">${r(n.label||"(no label)")}</div>
        <div class="inbox-preview">${r(d)}</div>
      </div>
      <div class="inbox-meta">
        <div class="inbox-time">${a}</div>
        <div class="inbox-badge" data-count="${n.unread}">${n.unread||""}</div>
      </div>
    </div>
  `}function q(n){const t=e.activeContact?.id===n.id&&e.screen==="chat",i=e.peerStatus[n.id]||"disconnected",a=n.latest?I(n.latest.timestamp):"",d=n.latest?n.latest.content.slice(0,35)+(n.latest.content.length>35?"…":""):"(no messages)";return`
    <div class="inbox-item ${t?"active":""}" data-contact-id="${n.id}">
      <div class="peer-dot ${i==="connected"?"connected":""}"></div>
      <div class="inbox-pin">${r(n.theirPin)}</div>
      <div class="inbox-info">
        <div class="inbox-label">${r(n.label||n.theirNumber)}</div>
        <div class="inbox-preview">${r(d)}</div>
      </div>
      <div class="inbox-meta">
        <div class="inbox-time">${a}</div>
        <div class="inbox-badge" data-count="${n.unread}">${n.unread||""}</div>
      </div>
    </div>
  `}function B(){switch(e.screen){case"welcome":return S();case"chat":return K();case"newPin":return T();case"pinMenu":return H();case"connect":return D();case"agentExport":return j();case"requests":return O();case"requestChat":return A()}}function S(){return`
    <div class="welcome">
      <pre class="welcome-logo">
 ██████╗ ██╗  ██╗██████╗
██╔═══██╗╚██╗██╔╝██╔══██╗
██║   ██║ ╚███╔╝ ██║  ██║
██║   ██║ ██╔██╗ ██║  ██║
╚██████╔╝██╔╝ ██╗██████╔╝
 ╚═════╝ ╚═╝  ╚═╝╚═════╝</pre>
      <div class="welcome-hint">// select a pin from inbox to start chatting</div>
    </div>
  `}function K(){const n=e.activePin,t=e.activeContact,i=n?e.messages[n.id]||[]:t?e.contactMessages[t.id]||[]:[],a=n?n.id:t?.id||"",d=e.peerStatus[a]||"disconnected",s=r(n?n.label||n.value:t?t.label||t.theirNumber:""),o=n?`// pin: ${r(n.value)} &nbsp;·&nbsp; ${r(d)}`:t?`// ${r(t.theirNumber)} &nbsp;·&nbsp; pin: ${r(t.theirPin)} &nbsp;·&nbsp; ${r(d)}`:"";return`
    <div style="display:flex;flex-direction:column;height:100%">
      <div class="chat-header">
        <div style="flex:1">
          <div class="chat-name">${s}</div>
          <div class="chat-pin-label">${o}</div>
        </div>
        ${n?'<button class="chat-menu-btn" id="btn-pin-menu">⋯</button>':'<button class="chat-menu-btn" id="btn-contact-remove" title="削除">✕</button>'}
      </div>
      <div class="messages-area" id="messages-area">
        ${i.map(u=>M(u)).join("")}
      </div>
      <div class="chat-input-area">
        <textarea
          class="chat-input"
          id="chat-input"
          placeholder="メッセージ..."
          rows="1"
        ></textarea>
        <button class="send-btn" id="btn-send">▶</button>
      </div>
    </div>
  `}function M(n){const t=n.isMine?"mine":"theirs",i=new Date(n.timestamp).toLocaleTimeString("ja-JP",{hour:"2-digit",minute:"2-digit"});let a="";return n.isMine&&(n.status==="queued"?a='<span class="msg-status-queued"> // waiting…</span>':n.status==="delivered"&&(a='<span class="msg-status-delivered"> ✓</span>')),`
    <div class="msg ${t}" data-local-id="${n.localId||""}">
      <div class="msg-bubble">${r(n.content)}</div>
      <div class="msg-time">${i}${a}</div>
    </div>
  `}function T(){const n=[{value:"none",label:"なし"},{value:"24h",label:"24h"},{value:"1w",label:"1週間"},{value:"once",label:"1回のみ"},{value:"custom",label:"カスタム"}],t=e.newPinExpiry==="custom";return`
    <div class="newpin-panel">
      <div class="section-label">// new_pin</div>
      <div class="pin-display">
        <div class="pin-value" id="new-pin-display">${e.newPinValue}</div>
        <div class="pin-hint">相手に渡すPINです</div>
      </div>
      <div class="form-group">
        <div class="form-label">// label（任意）</div>
        <input class="form-input" id="pin-label-input" type="text" placeholder="例: フリマ用、田中さん...">
      </div>
      <div class="form-group">
        <div class="form-label">// expiry</div>
        <div class="expiry-grid">
          ${n.map(i=>`
            <button class="expiry-opt ${e.newPinExpiry===i.value?"selected":""}"
              data-expiry="${i.value}">${i.label}</button>
          `).join("")}
        </div>
        ${t?`
        <div class="expiry-custom">
          <input class="expiry-custom-num" id="expiry-custom-num" type="number" min="1" max="999"
            value="${e.newPinCustomNum}">
          <select class="expiry-custom-unit" id="expiry-custom-unit">
            <option value="h" ${e.newPinCustomUnit==="h"?"selected":""}>時間</option>
            <option value="d" ${e.newPinCustomUnit==="d"?"selected":""}>日</option>
            <option value="w" ${e.newPinCustomUnit==="w"?"selected":""}>週間</option>
          </select>
        </div>
        `:""}
      </div>
      <div class="form-group">
        <div class="form-label">// type</div>
        <div class="expiry-grid" style="grid-template-columns: 1fr 1fr">
          <button class="expiry-opt ${e.newPinIsLobby?"":"selected"}" id="type-direct">通常</button>
          <button class="expiry-opt ${e.newPinIsLobby?"selected":""}" id="type-lobby">公開用</button>
        </div>
        ${e.newPinIsLobby?'<div style="padding:6px 0; font-size:10px; color:var(--text-muted)">// 名刺・SNS公開用。メッセージは requests に届き、返信した時点で専用受信箱に昇格します</div>':""}
      </div>
      <button class="ghost-btn" id="btn-regen-pin">// GENERATE_NEW →</button>
      <button class="primary-btn" id="btn-save-pin">// SAVE_AND_USE →</button>
    </div>
  `}function D(){return`
    <div class="newpin-panel">
      <div class="section-label">// connect_to_peer</div>
      <div class="form-group">
        <div class="form-label">// their_number</div>
        <input class="form-input" id="connect-number" type="text" placeholder="0x0-NNN-NNNN-NNNN" autocomplete="off">
      </div>
      <div class="form-group">
        <div class="form-label">// pin</div>
        <input class="form-input" id="connect-pin" type="text" placeholder="a3f9" maxlength="16" autocomplete="off">
      </div>
      <div class="form-group">
        <div class="form-label">// label（任意）</div>
        <input class="form-input" id="connect-label" type="text" placeholder="例: 田中さん">
      </div>
      <button class="primary-btn" id="btn-do-connect">// CONNECT →</button>
    </div>
  `}function H(){const n=e.activePin;return`
    <div class="menu-panel">
      <div class="menu-pin-header">
        <div class="menu-pin-name">${r(n.label||n.value)}</div>
        <div class="menu-pin-sub">// pin: ${r(n.value)}</div>
      </div>
      <div class="menu-section-label">// pin_settings</div>
      <div class="menu-item" id="menu-rotate">
        <div>
          <div class="menu-item-label">PINを変更する</div>
          <div class="menu-item-sub">新しいPINを生成して渡し直す</div>
        </div>
        <div class="menu-item-arrow">›</div>
      </div>
      <div class="menu-item" id="menu-label">
        <div>
          <div class="menu-item-label">ラベルを編集</div>
          <div class="menu-item-sub">現在: ${r(n.label||"(なし)")}</div>
        </div>
        <div class="menu-item-arrow">›</div>
      </div>
      <div class="menu-section-label">// integrations</div>
      <div class="menu-item" id="menu-agent-export">
        <div>
          <div class="menu-item-label">エージェント接続</div>
          <div class="menu-item-sub">AIエージェント向けの接続設定を書き出す</div>
        </div>
        <div class="menu-item-arrow">›</div>
      </div>
      <div class="menu-section-label">// danger_zone</div>
      <div class="menu-item danger" id="menu-revoke">
        <div>
          <div class="menu-item-label">このPINを今すぐ無効化</div>
          <div class="menu-item-sub">相手からの受信が即時停止される</div>
        </div>
        <div class="menu-item-arrow">›</div>
      </div>
      <div style="padding: 16px 24px">
        <button class="ghost-btn" id="menu-back">← back</button>
      </div>
    </div>
  `}function O(){const n=e.activePin,t=e.lobbyThreads[n.id]||[];return`
    <div class="menu-panel">
      <div class="menu-pin-header">
        <div class="menu-pin-name">// requests</div>
        <div class="menu-pin-sub">pin: ${r(n.value)} · ${t.length} 件</div>
      </div>
      ${t.length===0?'<div style="padding:16px 24px; font-size:11px; opacity:0.4">// no requests yet</div>':t.map(i=>`
          <div class="menu-item request-thread-item" data-pubkey="${r(i.pubKeyHex)}">
            <div>
              <div class="menu-item-label" style="font-family:var(--mono); font-size:11px">${r(i.shortKey)}…</div>
              <div class="menu-item-sub">${i.latest?r(i.latest.content?.slice(0,40)||""):"(no messages)"}</div>
            </div>
            <div class="inbox-badge" data-count="${i.count}">${i.count||""}</div>
          </div>
        `).join("")}
      <div style="padding: 16px 24px">
        <button class="ghost-btn" id="requests-back">← back</button>
      </div>
    </div>
  `}function A(){const n=e.activePin,i=e.activeLobbyKey.slice(0,16),a=e.messages[n.id+":"+i]||[];return`
    <div style="display:flex;flex-direction:column;height:100%">
      <div class="chat-header">
        <div style="flex:1">
          <div class="chat-name">${r(i)}…</div>
          <div class="chat-pin-label">// request · pin: ${r(n.value)}</div>
        </div>
        <button class="chat-menu-btn" id="requests-chat-back" title="戻る">✕</button>
      </div>
      <div class="messages-area" id="messages-area">
        ${a.map(d=>`
          <div class="msg ${d.isMine?"mine":"theirs"}">
            <div class="msg-bubble">${r(d.content||"")}</div>
          </div>
        `).join("")}
      </div>
      <div class="chat-input-area">
        <textarea class="chat-input" id="request-chat-input" placeholder="返信すると承認されます..." rows="1"></textarea>
        <button class="send-btn" id="request-send-btn">▶</button>
      </div>
    </div>
  `}function j(){const n=e.activePin,t={provider:"0x0",number:e.number,pin:n.value,command:`npx 0x0-cli pipe ${e.number} ${n.value}`},i=JSON.stringify(t,null,2);return`
    <div class="menu-panel">
      <div class="menu-pin-header">
        <div class="menu-pin-name">// agent_connect</div>
        <div class="menu-pin-sub">pin: ${r(n.value)}${n.label?" &nbsp;·&nbsp; "+r(n.label):""}</div>
      </div>
      <div class="agent-export-body">
        <div class="agent-export-desc">
          AIエージェント（OpenClaw等）がこのPINで接続するための設定です。<br>
          以下の設定をエージェントのconfig（openclaw.json等）に貼り付けてください。
        </div>
        <div class="agent-config-block">
          <pre id="agent-config-pre">${r(i)}</pre>
        </div>
        <div class="agent-export-actions">
          <button class="primary-btn" id="btn-copy-config">// COPY CONFIG →</button>
          <div class="agent-copy-hint" id="agent-copy-hint"></div>
        </div>
        <div class="agent-export-hint">
          <div>// how to use</div>
          <div style="margin-top:8px;opacity:0.6;font-size:0.78rem">
            1. エージェントが <code>command</code> を子プロセスとして起動する<br>
            2. stdin に JSON コマンドを送る<br>
            3. stdout から JSON イベントを受け取る<br>
            4. 詳細: <a href="https://0x0.contact/doc#openclaw" target="_blank" style="color:#888">0x0.contact/doc</a>
          </div>
        </div>
      </div>
      <div style="padding: 16px 24px">
        <button class="ghost-btn" id="agent-export-back">← back</button>
      </div>
    </div>
  `}function _(){document.getElementById("theme-toggle")?.addEventListener("click",()=>{e.theme=e.theme==="dark"?"light":"dark",document.documentElement.classList.toggle("light",e.theme==="light"),c()}),document.getElementById("btn-copy")?.addEventListener("click",()=>{navigator.clipboard.writeText(e.number).catch(()=>{})}),document.getElementById("btn-renew")?.addEventListener("click",()=>{confirm("番号を再発行しますか？全てのPINが無効になります。")&&l.send("number.renew")}),document.getElementById("btn-new-pin")?.addEventListener("click",()=>{e.screen="newPin",e.newPinValue=b(),c()}),document.getElementById("btn-connect")?.addEventListener("click",()=>{e.screen="connect",e.activePin=null,e.activeContact=null,c()}),document.querySelectorAll(".inbox-item[data-pin-id]").forEach(s=>{s.addEventListener("click",()=>{const o=s.dataset.pinId,u=e.inbox.find(m=>m.id===o);u&&(e.activePin=u,e.activeContact=null,u.type==="lobby"?(e.screen="requests",c(),l.send("messages.list",{pinId:o})):(e.screen="chat",c(),l.send("messages.list",{pinId:o}),v()))})}),document.querySelectorAll(".inbox-item[data-contact-id]").forEach(s=>{s.addEventListener("click",()=>{const o=s.dataset.contactId,u=e.contacts.find(m=>m.id===o);u&&(e.activeContact=u,e.activePin=null,e.screen="chat",c(),l.send("chat.start",{theirNumber:u.theirNumber,theirPin:u.theirPin,label:u.label}),v())})}),document.getElementById("btn-pin-menu")?.addEventListener("click",()=>{e.screen="pinMenu",c()}),document.getElementById("btn-contact-remove")?.addEventListener("click",()=>{e.activeContact&&confirm(`${e.activeContact.label||e.activeContact.theirNumber} を削除しますか？`)&&(l.send("contact.remove",{contactId:e.activeContact.id}),e.activeContact=null,e.screen="welcome",c())});const n=document.getElementById("chat-input"),t=()=>{const s=n?.value.trim();if(s){if(e.activePin){const o=e.activePin.id,u=crypto.randomUUID();e.messages[o]||(e.messages[o]=[]),e.messages[o].push({localId:u,content:s,isMine:!0,timestamp:Date.now(),status:"queued"}),l.send("message.send",{pinId:o,content:s,localId:u}),c(),v()}else e.activeContact&&l.send("contact.message.send",{contactId:e.activeContact.id,content:s});n.value="",n.style.height="auto"}};document.getElementById("btn-send")?.addEventListener("click",t),n?.addEventListener("keydown",s=>{s.key==="Enter"&&!s.shiftKey&&(s.preventDefault(),t())}),n?.addEventListener("input",()=>{n&&(n.style.height="auto",n.style.height=Math.min(n.scrollHeight,100)+"px")}),document.querySelectorAll(".expiry-opt").forEach(s=>{s.addEventListener("click",()=>{e.newPinExpiry=s.dataset.expiry||"none",c()})}),document.getElementById("expiry-custom-num")?.addEventListener("input",s=>{e.newPinCustomNum=s.target.value}),document.getElementById("expiry-custom-unit")?.addEventListener("change",s=>{e.newPinCustomUnit=s.target.value}),document.getElementById("type-direct")?.addEventListener("click",()=>{e.newPinIsLobby=!1,c()}),document.getElementById("type-lobby")?.addEventListener("click",()=>{e.newPinIsLobby=!0,c()}),document.getElementById("btn-regen-pin")?.addEventListener("click",()=>{e.newPinValue=b();const s=document.getElementById("new-pin-display");s&&w(s,e.newPinValue)}),document.getElementById("btn-save-pin")?.addEventListener("click",()=>{const s=document.getElementById("pin-label-input")?.value.trim()||"",o=document.getElementById("expiry-custom-num")?.value||e.newPinCustomNum,u=document.getElementById("expiry-custom-unit")?.value||e.newPinCustomUnit,m=e.newPinExpiry==="custom"?`${o}${u}`:e.newPinExpiry;l.send("pin.create",{label:s,expiry:m,type:e.newPinIsLobby?"lobby":"direct"}),e.screen="welcome",e.newPinExpiry="none",e.newPinIsLobby=!1,c()}),document.getElementById("btn-do-connect")?.addEventListener("click",()=>{const s=document.getElementById("connect-number")?.value.trim(),o=document.getElementById("connect-pin")?.value.trim(),u=document.getElementById("connect-label")?.value.trim()||"";!s||!o||l.send("chat.start",{theirNumber:s,theirPin:o,label:u})}),document.getElementById("menu-rotate")?.addEventListener("click",()=>{e.activePin&&(l.send("pin.rotate",{pinId:e.activePin.id}),e.screen="welcome",e.activePin=null,c())}),document.getElementById("menu-revoke")?.addEventListener("click",()=>{e.activePin&&(l.send("pin.revoke",{pinId:e.activePin.id}),e.screen="welcome",e.activePin=null,c())}),document.getElementById("menu-back")?.addEventListener("click",()=>{e.screen="chat",c()}),document.getElementById("menu-agent-export")?.addEventListener("click",()=>{e.screen="agentExport",c()}),document.getElementById("agent-export-back")?.addEventListener("click",()=>{e.screen="pinMenu",c()}),document.getElementById("btn-copy-config")?.addEventListener("click",()=>{const s=document.getElementById("agent-config-pre"),o=document.getElementById("agent-copy-hint");s&&navigator.clipboard.writeText(s.textContent||"").then(()=>{o&&(o.textContent="// copied!",setTimeout(()=>{o&&(o.textContent="")},2e3))}).catch(()=>{})}),document.getElementById("menu-label")?.addEventListener("click",()=>{const s=prompt("新しいラベル:",e.activePin?.label||"");s!==null&&e.activePin&&l.send("pin.label",{pinId:e.activePin.id,label:s})}),document.querySelectorAll(".request-thread-item").forEach(s=>{s.addEventListener("click",()=>{const o=s.dataset.pubkey;if(!o||!e.activePin)return;const u=o.slice(0,16);e.messages[e.activePin.id+":"+u]||(e.messages[e.activePin.id+":"+u]=[]),e.activeLobbyKey=o,e.screen="requestChat",c(),v()})}),document.getElementById("requests-back")?.addEventListener("click",()=>{e.screen="welcome",e.activePin=null,c()}),document.getElementById("requests-chat-back")?.addEventListener("click",()=>{e.screen="requests",e.activeLobbyKey=null,c()});const i=document.getElementById("request-send-btn"),a=document.getElementById("request-chat-input");i?.addEventListener("click",()=>d()),a?.addEventListener("keydown",s=>{s.key==="Enter"&&!s.shiftKey&&(s.preventDefault(),d())});function d(){const s=document.getElementById("request-chat-input"),o=s?.value.trim();if(!o||!e.activePin||!e.activeLobbyKey)return;const u=e.activePin,m=e.activeLobbyKey,P=m.slice(0,16),y=String(Date.now()),h=u.id+":"+P,f=e.messages[h]||[];f.push({localId:y,content:o,isMine:!0,timestamp:Date.now(),status:"queued"}),e.messages[h]=f,l.send("message.send",{pinId:u.id,content:o,pubKeyHex:m,localId:y}),s&&(s.value="",s.style.height="auto"),c(),v()}}l.on("init",n=>{const t=n;e.number=t.data.number,e.inbox=t.data.inbox,e.contacts=t.data.contacts||[],t.data.prefs?.theme==="light"&&(e.theme="light",document.documentElement.classList.add("light")),c(),E()});l.on("inbox.list",n=>{const t=n;if(e.inbox=t.data,e.activePin){const i=t.data.find(a=>a.id===e.activePin.id);i&&(e.activePin=i)}c()});l.on("contacts.list",n=>{const t=n;if(e.contacts=t.data,e.activeContact){const i=t.data.find(a=>a.id===e.activeContact.id);i&&(e.activeContact=i)}c()});l.on("messages.list",n=>{const t=n;e.messages[t.pinId]=t.data,p(t.pinId,!0)});l.on("chat.started",n=>{const t=n,i=e.contacts.findIndex(a=>a.id===t.contactId);i===-1?e.contacts.push(t.data):e.contacts[i]={...e.contacts[i],...t.data},e.activeContact=e.contacts.find(a=>a.id===t.contactId)||t.data,e.activePin=null,e.screen="chat",c(),v()});l.on("contact.messages.list",n=>{const t=n;e.contactMessages[t.contactId]=t.data,g(t.contactId)});l.on("message.received",n=>{const t=n;e.messages[t.pinId]||(e.messages[t.pinId]=[]),e.messages[t.pinId].push(t.data);const i=e.inbox.find(a=>a.id===t.pinId);i&&(i.unread++,i.latest=t.data),p(t.pinId,!0)});l.on("contact.message.received",n=>{const t=n;e.contactMessages[t.contactId]||(e.contactMessages[t.contactId]=[]),e.contactMessages[t.contactId].push(t.data);const i=e.contacts.find(a=>a.id===t.contactId);i&&(i.unread++,i.latest=t.data),g(t.contactId)});l.on("message.sent",n=>{const t=n;t.localId?x(t.pinId,t.localId,"delivered"):(e.messages[t.pinId]||(e.messages[t.pinId]=[]),e.messages[t.pinId].push(t.data)),p(t.pinId,!0)});l.on("message.queued",()=>{});l.on("message.delivered",n=>{const t=n;x(t.pinId,t.localId,"delivered"),p(t.pinId,!1)});l.on("contact.message.sent",n=>{const t=n;e.contactMessages[t.contactId]||(e.contactMessages[t.contactId]=[]),e.contactMessages[t.contactId].push(t.data),g(t.contactId)});l.on("peer.status",n=>{const t=n,i=t.pinId||t.contactId||"";i&&(e.peerStatus[i]=t.status),c()});l.on("pin.created",()=>{l.send("inbox.list")});l.on("pin.rotated",()=>{l.send("inbox.list")});l.on("pin.revoked",()=>{l.send("inbox.list")});l.on("contact.removed",n=>{const t=n;e.contacts=e.contacts.filter(i=>i.id!==t.contactId),delete e.contactMessages[t.contactId],delete e.peerStatus[t.contactId],c()});l.on("lobby.threads",n=>{const t=n;e.lobbyThreads[t.pinId]=t.data.map(i=>({...i,shortKey:i.pubKeyHex.slice(0,16)})),e.screen==="requests"&&e.activePin?.id===t.pinId&&c()});l.on("lobby.connected",n=>{const t=n,i=e.lobbyThreads[t.pinId]||[];i.find(a=>a.pubKeyHex===t.pubKeyHex)||(i.push({pubKeyHex:t.pubKeyHex,shortKey:t.pubKeyHex.slice(0,16),latest:null,count:0}),e.lobbyThreads[t.pinId]=i),e.screen==="requests"&&(e.activePin?.id,t.pinId),c()});l.on("lobby.message",n=>{const t=n,i=t.pinId+":"+t.shortKey,a=e.messages[i]||[];a.push({...t.data,id:String(Date.now())}),e.messages[i]=a;const s=(e.lobbyThreads[t.pinId]||[]).find(o=>o.pubKeyHex===t.pubKeyHex);s&&(s.latest=t.data,s.count++),e.screen==="requestChat"&&e.activePin?.id===t.pinId&&e.activeLobbyKey===t.pubKeyHex?(c(),v()):(e.screen==="requests"&&(e.activePin?.id,t.pinId),c())});l.on("lobby.migrated",n=>{const t=n;l.send("inbox.list"),e.activePin?.id===t.pinId&&(e.screen==="requestChat"||e.screen==="requests")&&(e.screen="welcome",e.activePin=null,e.activeLobbyKey=null,c())});l.on("number.renewed",n=>{const t=n;e.number=t.data.number,c(),E()});function x(n,t,i){const a=e.messages[n]||[],d=a.findIndex(s=>s.localId===t);d!==-1&&(a[d]={...a[d],status:i},e.messages[n]=a)}function p(n,t){e.screen==="chat"&&e.activePin?.id===n?(c(),t&&v()):c()}function g(n,t){e.screen==="chat"&&e.activeContact?.id===n?(c(),v()):c()}function v(){setTimeout(()=>{const n=document.getElementById("messages-area");n&&(n.scrollTop=n.scrollHeight)},0)}function I(n){const t=new Date(n),i=new Date;if(t.toDateString()===i.toDateString())return t.toLocaleTimeString("ja-JP",{hour:"2-digit",minute:"2-digit"});const a=new Date(i);return a.setDate(a.getDate()-1),t.toDateString()===a.toDateString()?"昨日":t.toLocaleDateString("ja-JP",{month:"numeric",day:"numeric"})}function r(n){return n.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#039;").replace(/\n/g,"<br>")}function w(n,t){const i="0123456789abcdef";let a=0;const d=setInterval(()=>{let s="";for(const o of t)s+=Math.random()<.3?i[Math.floor(Math.random()*i.length)]:o;n.textContent=s,++a>6&&(clearInterval(d),n.textContent=t)},70)}function E(){const n=document.getElementById("my-number");n&&e.number&&w(n,e.number)}l.connect();c();
