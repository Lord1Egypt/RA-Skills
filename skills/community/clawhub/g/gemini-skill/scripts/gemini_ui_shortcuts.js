(function initGeminiOps(){
  const S = {
    promptInput: [
      'textarea[aria-label*="Gemini"]',
      'textarea[placeholder*="Gemini"]',
      'div[contenteditable="true"]'
    ],
    sendBtn: [
      'button[aria-label*="发送"]',
      'button[aria-label*="Send"]',
      'button:has-text("发送")'
    ],
    imageToggle: [
      'button:has-text("图片")',
      'button:has-text("生成图片")',
      '[role="button"]:has-text("Image")'
    ],
    modelBtn: [
      'button:has-text("Gemini")',
      '[role="button"][aria-haspopup="menu"]'
    ]
  };

  function visible(el){
    if(!el) return false;
    const r=el.getBoundingClientRect();
    const st=getComputedStyle(el);
    return r.width>0 && r.height>0 && st.display!=='none' && st.visibility!=='hidden';
  }

  function q(sel){
    try{
      if(sel.includes(':has-text(')){
        const m=sel.match(/^(.*):has-text\("(.*)"\)$/);
        if(!m) return null;
        const nodes=[...document.querySelectorAll(m[1]||'*')];
        return nodes.find(n=>visible(n)&&n.textContent?.includes(m[2]))||null;
      }
      return [...document.querySelectorAll(sel)].find(visible)||null;
    }catch{return null;}
  }

  function find(key){
    for(const s of (S[key]||[])){
      const el=q(s);
      if(el) return el;
    }
    return null;
  }

  function click(key){
    const el=find(key);
    if(!el) return {ok:false,key,error:'not_found'};
    el.click();
    return {ok:true,key};
  }

  function fillPrompt(text){
    const el=find('promptInput');
    if(!el) return {ok:false,error:'prompt_not_found'};
    el.focus();
    if(el.tagName==='TEXTAREA'){
      el.value=text;
      el.dispatchEvent(new Event('input',{bubbles:true}));
    }else{
      document.execCommand('selectAll',false,null);
      document.execCommand('insertText',false,text);
      el.dispatchEvent(new Event('input',{bubbles:true}));
    }
    return {ok:true};
  }

  function probe(){
    return {
      promptInput: !!find('promptInput'),
      sendBtn: !!find('sendBtn'),
      imageToggle: !!find('imageToggle'),
      modelBtn: !!find('modelBtn')
    };
  }

  window.GeminiOps = {probe, click, fillPrompt, selectors:S, version:'0.1.0'};
})();
