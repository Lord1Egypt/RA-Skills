    // Config injected by server
    const CONFIG = window.__RT_CONFIG__ || { token: '', port: 8199, host: '0.0.0.0' };
    const API_BASE = '';

    // State
    let state = {
      status: 'waiting',
      speeches: [],
      participants: [],
      topic: '',
      conclusion: null,
      currentRound: 0,
      speechIdSet: new Set(),
      roundSummaries: [],
      roundSummarySet: new Set(),
      streamSpeechMap: new Map(),
    };

    // Token batching buffer (rAF-based)
    let tokenBuffer = [];
    let rafId = null;

    // Auto-scroll state
    let autoScrollEnabled = true;
    const SCROLL_THRESHOLD = 50;


    // DOM refs
    const $statusBadge = document.getElementById('statusBadge');
    const $statusLabel = document.getElementById('statusLabel');
    const $topicTitle = document.getElementById('topicTitle');
    const $connDot = document.getElementById('connDot');
    const $connText = document.getElementById('connText');
    const $waitingState = document.getElementById('waitingState');
    const $activeState = document.getElementById('activeState');
    const $speechesContainer = document.getElementById('speechesContainer');
    let activeSpeechesContainer = $speechesContainer;
    const $participantsBar = document.getElementById('participantsBar');
    const $conclusionCard = document.getElementById('conclusionCard');
    const $conclusionContent = document.getElementById('conclusionContent');
    const $revokedState = document.getElementById('revokedState');
    const $scrollBottomBtn = document.getElementById('scrollBottomBtn');

    // ---- Auto-scroll logic ----
    const mainEl = document.querySelector('main');

    mainEl?.addEventListener('scroll', () => {
      const distanceFromBottom = mainEl.scrollHeight - mainEl.scrollTop - mainEl.clientHeight;
      autoScrollEnabled = distanceFromBottom < SCROLL_THRESHOLD;
      if ($scrollBottomBtn) {
        $scrollBottomBtn.classList.toggle('hidden', autoScrollEnabled);
      }
    });

    $scrollBottomBtn?.addEventListener('click', () => {
      mainEl?.scrollTo({ top: mainEl.scrollHeight, behavior: 'smooth' });
      autoScrollEnabled = true;
      $scrollBottomBtn.classList.add('hidden');
    });

    function scrollToEnd() {
      if (autoScrollEnabled && mainEl) {
        mainEl.scrollTop = mainEl.scrollHeight;
      }
    }

    // ---- SSE Connection ----
    let eventSource = null;
    let reconnectAttempts = 0;
    const MAX_RECONNECT_DELAY = 30000;

    function connectSSE() {
      const url = `${API_BASE}/api/${CONFIG.token}/events`;

      if (typeof EventSource !== 'undefined') {
        // SSE (primary)
        eventSource = new EventSource(url);

        eventSource.addEventListener('init', (e) => {
          const data = JSON.parse(e.data);
          handleData(data);
          setConnection('connected');
          reconnectAttempts = 0;
        });

        eventSource.addEventListener('update', (e) => {
          const data = JSON.parse(e.data);
          handleData(data);
        });

        eventSource.addEventListener('delta', (e) => {
          const data = JSON.parse(e.data);
          handleDelta(data);
        });

        eventSource.addEventListener('revoked', () => {
          showRevoked();
        });

        eventSource.onerror = () => {
          setConnection('reconnecting');
          eventSource.close();
          reconnectAttempts++;
          const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), MAX_RECONNECT_DELAY);
          setTimeout(connectSSE, delay);
        };
      } else {
        // Long-polling fallback (WeChat)
        startLongPolling();
      }
    }

    function startLongPolling() {
      let since = 0;

      async function poll() {
        try {
          const resp = await fetch(`${API_BASE}/api/${CONFIG.token}/poll?since=${since}`);
          if (resp.status === 403) { showRevoked(); return; }
          if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

          const data = await resp.json();
          if (data.updated_at > since) {
            since = data.updated_at;
            handleData(data);
          }
          setConnection('connected');
        } catch (err) {
          setConnection('disconnected');
          await new Promise(r => setTimeout(r, 3000));
        }

        poll(); // continue polling
      }

      poll();
    }

    // ---- Data handling ----
    function handleDelta(data) {
      const events = Array.isArray(data?.events) ? data.events : [];
      for (const eventData of events) {
        applyStreamEvent(eventData);
      }
      if (events.length > 0) {
        $waitingState.classList.add('hidden');
        $activeState.classList.remove('hidden');
      }
    }

    function applyStreamEvent(eventData) {
      if (!eventData || !eventData.type) return;
      if (eventData.type === 'speech_start') {
        renderStreamingSpeechStart(eventData);
      } else if (eventData.type === 'speech_token') {
        appendStreamingSpeechToken(eventData);
      } else if (eventData.type === 'speech_end') {
        markStreamingSpeechEnd(eventData);
      } else if (eventData.type === 'speech_delta') {
        const speech = eventData.speech || eventData.payload?.speech;
        if (speech) mergeSpeech(speech, true);
      } else if (eventData.type === 'status_delta') {
        if (eventData.status || eventData.payload?.status) {
          state.status = eventData.status || eventData.payload.status;
          updateStatusUI();
        }
        const conclusion = eventData.conclusion || eventData.payload?.conclusion;
        if (conclusion && !state.conclusion) {
          state.conclusion = conclusion;
          renderConclusion(conclusion);
        }
      } else if (eventData.type === 'round_summary') {
        renderRoundSummary(eventData);
      } else if (eventData.type === 'final_summary') {
        renderFinalSummary(eventData);
      }
    }

    function handleData(data) {
      if (data.status === 'revoked' || (data.revoked_tokens && data.revoked_tokens.includes(CONFIG.token))) {
        showRevoked();
        return;
      }

      // Update topic
      if (data.topic && data.topic !== state.topic) {
        state.topic = data.topic;
        $topicTitle.textContent = data.topic;
        document.title = `${data.topic} — 圆桌讨论`;
      }

      // Update participants
      if (data.participants) {
        state.participants = data.participants;
        renderParticipants();
      }

      // Update speeches
      if (data.speeches) {
        const isInitialLoad = state.speeches.length === 0;
        for (const speech of data.speeches) {
          mergeSpeech(speech, !isInitialLoad);
        }

        // If it was the initial load, collapse older rounds
        if (isInitialLoad && state.speeches.length > 0) {
          const rounds = [...new Set(state.speeches.map(s => s.round))].sort((a, b) => a - b);
          if (rounds.length > 1) {
            const latestRound = rounds[rounds.length - 1];
            for (const r of rounds) {
              if (r !== latestRound) {
                const section = document.getElementById(`round-section-${r}`);
                if (section) {
                  section.classList.add('collapsed');
                }
              }
            }
          }
        }
      }

      // Update status
      if (data.status !== state.status) {
        state.status = data.status;
        updateStatusUI();
      }

      // Conclusion
      if (data.conclusion && !state.conclusion) {
        state.conclusion = data.conclusion;
        renderConclusion(data.conclusion);
      }

      // Round summaries / viewpoint cards
      if (Array.isArray(data.round_summaries)) {
        for (const summary of data.round_summaries) {
          renderRoundSummary(summary);
        }
      }

      if (data.final_summary) {
        renderFinalSummary(data.final_summary);
      }

      // Show active state if we have speeches or viewpoint cards
      if ((state.speeches.length > 0 || state.roundSummaries.length > 0) && state.status !== 'waiting') {
        $waitingState.classList.add('hidden');
        $activeState.classList.remove('hidden');
      }
    }

    // ---- Helper functions for role styles and aggregation ----
    function getRoleType(roleStr) {
      if (!roleStr) return 'default';
      const r = roleStr.toLowerCase();
      if (r.includes('product') || r.includes('pm') || r.includes('director') || r.includes('经理') || r.includes('总监')) return 'product';
      if (r.includes('design') || r.includes('ui') || r.includes('ux') || r.includes('设计')) return 'design';
      if (r.includes('engineer') || r.includes('dev') || r.includes('coder') || r.includes('tech') || r.includes('开发') || r.includes('工程') || r.includes('技术')) return 'engineer';
      if (r.includes('research') || r.includes('science') || r.includes('sci') || r.includes('researcher') || r.includes('研究') || r.includes('分析')) return 'research';
      if (r.includes('marketing') || r.includes('sales') || r.includes('biz') || r.includes('运营') || r.includes('市场')) return 'marketing';
      return 'default';
    }

    // Sprint 3: Agent 人格可视化辅助函数
    function getParticipantAvatar(agent) {
      if (agent === 'coordinator') return '📋';
      const p = state.participants.find(x => x.profile === agent || x.participant === agent);
      if (p && p.avatar) return p.avatar;
      const role = (p && p.role) ? p.role.toLowerCase() : '';
      if (role.includes('design') || role.includes('设计')) return '🎨';
      if (role.includes('product') || role.includes('产品') || role.includes('总监')) return '📦';
      if (role.includes('engineer') || role.includes('tech') || role.includes('技术') || role.includes('开发')) return '⚡';
      if (role.includes('research') || role.includes('研究')) return '🔬';
      return '🤖';
    }

    function getRoleTagClass(roleType) {
      const map = { engineer: 'role-tech', product: 'role-product', design: 'role-design', coordinator: 'role-coord' };
      return map[roleType] || 'role-default';
    }

    // Agent 信息浮层
    let agentInfoPopup = null;
    let agentInfoTimeout = null;

    function showAgentInfo(agent, anchorEl) {
      hideAgentInfo();
      const p = state.participants.find(x => x.profile === agent || x.participant === agent);
      const avatar = getParticipantAvatar(agent);
      const name = (p && p.display_name) || agent || 'Agent';
      const role = (p && p.role) || '';
      const desc = (p && p.description) || '';
      const agentId = agent || 'unknown';
      const speechCount = state.speeches ? state.speeches.filter(s => s.participant === agentId).length : 0;
      const roundCount = new Set((state.speeches || []).filter(s => s.participant === agentId).map(s => s.round)).size;

      const popup = document.createElement('div');
      popup.className = 'agent-info-popup';
      popup.innerHTML = `
        <div class="agent-info-header">
          <div class="agent-info-avatar speaker-avatar" style="cursor:default">${avatar}</div>
          <div>
            <div class="agent-info-name">${escapeHtml(name)}</div>
            ${role ? `<div class="agent-info-role">${escapeHtml(role)}</div>` : ''}
          </div>
        </div>
        ${desc ? `<div class="agent-info-desc">${escapeHtml(desc)}</div>` : ''}
        <div class="agent-info-stats">
          <div class="agent-stat"><div class="agent-stat-value">${speechCount}</div><div class="agent-stat-label">发言</div></div>
          <div class="agent-stat"><div class="agent-stat-value">${roundCount}</div><div class="agent-stat-label">轮次</div></div>
        </div>
      `;
      document.body.appendChild(popup);
      agentInfoPopup = popup;

      // 定位
      const rect = anchorEl.getBoundingClientRect();
      let left = rect.left;
      let top = rect.bottom + 8;
      if (left + 280 > window.innerWidth) left = window.innerWidth - 290;
      if (top + 200 > window.innerHeight) top = rect.top - 208;
      popup.style.left = Math.max(8, left) + 'px';
      popup.style.top = Math.max(8, top) + 'px';

      // 点击外部关闭
      setTimeout(() => {
        document.addEventListener('click', hideAgentInfoOnClick);
      }, 50);
    }

    function hideAgentInfo() {
      if (agentInfoPopup) {
        agentInfoPopup.remove();
        agentInfoPopup = null;
      }
      document.removeEventListener('click', hideAgentInfoOnClick);
    }

    function hideAgentInfoOnClick(e) {
      if (agentInfoPopup && !agentInfoPopup.contains(e.target)) {
        hideAgentInfo();
      }
    }

    function escapeHtml(value) {
      return String(value ?? '').replace(/[&<>"']/g, ch => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
      })[ch]);
    }

    function renderMarkdown(value) {
      const html = marked.parse(String(value ?? ''));
      if (window.DOMPurify) {
        return DOMPurify.sanitize(html);
      }
      const template = document.createElement('template');
      template.innerHTML = html;
      template.content.querySelectorAll('script, iframe, object, embed, link, meta').forEach(el => el.remove());
      template.content.querySelectorAll('*').forEach(el => {
        for (const attr of [...el.attributes]) {
          if (/^on/i.test(attr.name) || /javascript:/i.test(attr.value)) {
            el.removeAttribute(attr.name);
          }
        }
      });
      return template.innerHTML;
    }

    window.toggleRound = function(id) {
      const section = document.getElementById(id);
      if (section) {
        section.classList.toggle('collapsed');
      }
    };

    function getOrCreateRoundSection(roundNum, isNew) {
      const prefix = activeSpeechesContainer ? activeSpeechesContainer.id : 'speechesContainer';
      const id = `${prefix}-round-section-${roundNum}`;
      let section = document.getElementById(id);
      if (!section) {
        section = document.createElement('div');
        section.id = id;
        section.className = 'round-section';
        
        const titleText = roundNum === 0 ? '📢 开场发言 (Round 0)' : `💬 第 ${roundNum} 轮讨论 (Round ${roundNum})`;
        
        section.innerHTML = `
          <div class="round-header" onclick="toggleRound('${id}')">
            <div class="round-title">
              <span>${titleText}</span>
              <span class="round-badge-count" id="${prefix}-round-count-${roundNum}">0 条发言</span>
            </div>
            <svg class="toggle-icon" viewBox="0 0 24 24">
              <path d="M19 9l-7 7-7-7" />
            </svg>
          </div>
          <div class="round-body" id="${prefix}-round-body-${roundNum}"></div>
        `;
        
        // Collapse all previous rounds if it's dynamic update (isNew)
        if (isNew && activeSpeechesContainer) {
          const existingSections = activeSpeechesContainer.querySelectorAll('.round-section');
          existingSections.forEach(s => s.classList.add('collapsed'));
        }
        
        if (activeSpeechesContainer) {
          activeSpeechesContainer.appendChild(section);
        }
      }
      return section;
    }

    // ---- Rendering ----
    function renderParticipants() {
      $participantsBar.innerHTML = state.participants.map(p => {
        const agent = p.profile || p.participant || '';
        const avatar = getParticipantAvatar(agent);
        const name = escapeHtml(p.display_name || p.profile || '?');
        const roleType = getRoleType(p.role || '');
        const speechCount = state.speeches ? state.speeches.filter(s => s.participant === agent).length : 0;
        return `<div class="participant-chip" data-agent="${escapeHtml(agent)}" onclick="event.stopPropagation(); showAgentInfo('${escapeHtml(agent)}', this)">
          <span class="chip-avatar">${avatar}</span>
          <span class="font-medium" style="color:var(--rt-text-primary)">${name}</span>
          ${p.role ? `<span class="speaker-role-tag ${getRoleTagClass(roleType)}">${escapeHtml(p.role)}</span>` : ''}
          ${speechCount > 0 ? `<span class="chip-count">${speechCount}</span>` : ''}
        </div>`;
      }).join('');

      // 更新移动端触发按钮
      const $triggerAvatars = document.getElementById('triggerAvatars');
      const $triggerCount = document.getElementById('triggerCount');
      if ($triggerAvatars) {
        $triggerAvatars.innerHTML = state.participants.slice(0, 4).map(p => {
          const agent = p.profile || p.participant || '';
          return `<span>${getParticipantAvatar(agent)}</span>`;
        }).join('');
      }
      if ($triggerCount) {
        $triggerCount.textContent = `${state.participants.length} 位参与者`;
      }

      // 更新移动端抽屉内容
      const $drawerList = document.getElementById('drawerParticipantList');
      if ($drawerList) {
        $drawerList.innerHTML = state.participants.map(p => {
          const agent = p.profile || p.participant || '';
          const avatar = getParticipantAvatar(agent);
          const name = escapeHtml(p.display_name || p.profile || '?');
          const role = p.role || '';
          const desc = p.description || '';
          const speechCount = state.speeches ? state.speeches.filter(s => s.participant === agent).length : 0;
          return `<div class="drawer-participant-item" onclick="toggleParticipantsDrawer(); showAgentInfo('${escapeHtml(agent)}', this)">
            <div class="speaker-avatar" style="cursor:pointer">${avatar}</div>
            <div class="drawer-participant-info">
              <div class="dp-name">${name}</div>
              ${role ? `<div class="dp-role">${escapeHtml(role)}</div>` : ''}
              ${desc ? `<div class="dp-desc">${escapeHtml(desc)}</div>` : ''}
            </div>
            ${speechCount > 0 ? `<span class="chip-count" style="font-size:13px">${speechCount} 条</span>` : ''}
          </div>`;
        }).join('');
      }
    }

    function toggleParticipantsDrawer() {
      const overlay = document.getElementById('participantsDrawerOverlay');
      const drawer = document.getElementById('participantsDrawer');
      if (!overlay || !drawer) return;
      const isOpen = drawer.classList.contains('open');
      if (isOpen) {
        drawer.classList.remove('open');
        overlay.classList.remove('open');
      } else {
        drawer.classList.add('open');
        overlay.classList.add('open');
      }
    }

    function participantMeta(agent) {
      const participantObj = state.participants.find(p => p.profile === agent || p.participant === agent);
      const isCoordinator = agent === 'coordinator';
      const roleType = isCoordinator ? 'coordinator' : getRoleType(participantObj?.role || '');
      const defaultAvatars = { coordinator: '📋', design: '🎨', product: '📦', engineer: '⚡', research: '🔬', marketing: '📣', default: '🤖' };
      return {
        name: participantObj?.display_name || agent || 'Agent',
        role: participantObj?.role || '',
        roleType,
        avatar: participantObj?.avatar || (isCoordinator ? '📋' : (defaultAvatars[roleType] || '🤖')),
        title: participantObj?.title || '',
        description: participantObj?.description || '',
      };
    }

    function updateRoundCount(roundNum) {
      const prefix = activeSpeechesContainer ? activeSpeechesContainer.id : 'speechesContainer';
      const body = document.getElementById(`${prefix}-round-body-${roundNum}`);
      const countEl = document.getElementById(`${prefix}-round-count-${roundNum}`);
      if (body && countEl) {
        const count = body.querySelectorAll('.speech-card').length;
        countEl.textContent = `${count} 条发言`;
      }
    }

    function renderStreamingSpeechStart(eventData) {
      const id = eventData.id;
      if (!id || state.streamSpeechMap.has(id)) return;
      const agent = eventData.agent || eventData.participant || '';
      const meta = participantMeta(agent);
      const roundNum = Number(eventData.round || 0);
      const div = document.createElement('div');
      div.className = `speech-card role-${meta.roleType} new highlight streaming`;
      div.id = `speech-${id}`;

      const avatar = getParticipantAvatar(agent);
      const speakerName = escapeHtml(meta.name);
      const safeRoleName = escapeHtml(meta.role);
      const round = roundNum > 0 ? `<span class="round-badge" style="background: var(--rt-role-${meta.roleType}-bg); color: var(--rt-role-${meta.roleType})">R${roundNum}</span>` : '';
      const roleTagClass = getRoleTagClass(meta.roleType);
      div.innerHTML = `
        <div class="flex items-start gap-3">
          <div class="speaker-avatar" style="background: var(--rt-role-${meta.roleType}-bg); border-color: var(--rt-role-${meta.roleType})" onclick="event.stopPropagation(); showAgentInfo('${escapeHtml(agent)}', this)">${avatar}</div>
          <div class="flex-1 min-w-0">
            <div class="speech-header-meta">
              <span class="speaker-name font-semibold text-sm" style="color:var(--rt-text-primary)">${speakerName}</span>
              ${meta.role ? `<span class="speaker-role-tag ${roleTagClass}">${safeRoleName}</span>` : ''}
              ${round}
              <span class="text-xs ml-auto" style="color:var(--rt-text-muted)">${formatTime(eventData.timestamp)}</span>
            </div>
            <div class="text-sm leading-relaxed markdown-content stream-content stream-cursor" style="color:var(--rt-text-secondary)"></div>
          </div>
        </div>
      `;
      getOrCreateRoundSection(roundNum, true);
      const prefix = activeSpeechesContainer ? activeSpeechesContainer.id : 'speechesContainer';
      const body = document.getElementById(`${prefix}-round-body-${roundNum}`);
      if (body) body.appendChild(div);
      state.streamSpeechMap.set(id, { el: div, content: '', round: roundNum });
      updateRoundCount(roundNum);
      setTimeout(() => div.classList.remove('highlight'), 2000);
      scrollToEnd();
    }

    function appendStreamingSpeechToken(eventData) {
      tokenBuffer.push(eventData);
      if (!rafId) {
        rafId = requestAnimationFrame(flushTokenBuffer);
      }
    }

    function flushTokenBuffer() {
      rafId = null;
      const batch = tokenBuffer.splice(0);
      for (const eventData of batch) {
        const id = eventData.id;
        let entry = state.streamSpeechMap.get(id);
        if (!entry) {
          renderStreamingSpeechStart({ id, agent: eventData.agent || 'agent', round: eventData.round || state.currentRound || 0, timestamp: eventData.timestamp });
          entry = state.streamSpeechMap.get(id);
        }
        if (!entry) continue;
        entry.content += eventData.delta || '';
        const contentEl = entry.el.querySelector('.stream-content');
        if (contentEl) contentEl.innerHTML = renderMarkdown(entry.content);
      }
      scrollToEnd();
    }

    function markStreamingSpeechEnd(eventData) {
      const entry = state.streamSpeechMap.get(eventData.id);
      if (!entry) return;
      entry.el.classList.remove('streaming');
      const contentEl = entry.el.querySelector('.stream-content');
      if (contentEl) contentEl.classList.remove('stream-cursor');
      // 添加完成标记 ✓
      const headerEl = entry.el.querySelector('.flex.items-center');
      if (headerEl && !headerEl.querySelector('.speech-checkmark')) {
        const checkmark = document.createElement('span');
        checkmark.className = 'speech-checkmark';
        checkmark.textContent = '✓';
        checkmark.title = '发言完成';
        headerEl.appendChild(checkmark);
      }
    }

    function normalizeViewpointItems(items) {
      if (!Array.isArray(items)) return [];
      return items.map(item => typeof item === 'string' ? { content: item } : item).filter(Boolean);
    }

    function renderViewpointList(items, type) {
      const normalized = normalizeViewpointItems(items);
      if (normalized.length === 0) return '<li class="viewpoint-item">暂无</li>';
      return normalized.map(item => {
        const content = escapeHtml(item.content || item.text || item.title || String(item));
        const supporters = Array.isArray(item.supporters) && item.supporters.length > 0
          ? `<span class="viewpoint-supporters">支持：${escapeHtml(item.supporters.join('、'))}</span>`
          : '';
        return `<li class="viewpoint-item ${type}">${content}${supporters}</li>`;
      }).join('');
    }

    function renderRoundSummary(summary) {
      const roundNum = Number(summary.round || 0);
      const key = `round-${roundNum}`;
      state.roundSummarySet.add(key);
      state.roundSummaries = state.roundSummaries.filter(item => Number(item.round || 0) !== roundNum).concat(summary);
      getOrCreateRoundSection(roundNum, false);
      const prefix = activeSpeechesContainer ? activeSpeechesContainer.id : 'speechesContainer';
      const body = document.getElementById(`${prefix}-round-body-${roundNum}`);
      let card = document.getElementById(`viewpoints-${key}`);
      if (!card) {
        card = document.createElement('div');
        card.id = `viewpoints-${key}`;
        card.className = 'viewpoints-card';
        if (body) body.appendChild(card);
      }
      const consensus = summary.consensus || summary.consensus_points || [];
      const disagreement = summary.disagreement || summary.disagreement_points || [];
      const score = summary.convergence_score;
      const hasScore = score !== undefined && score !== null;
      const scorePercent = hasScore ? Math.round(Number(score) * 100) : 0;
      card.innerHTML = `
        <div class="viewpoints-title" onclick="this.parentElement.classList.toggle('collapsed')">
          <span>🧠 第 ${roundNum} 轮观点汇总</span>
          <span style="display:flex;align-items:center;gap:6px">
            ${hasScore ? `<span class="round-badge-count">收敛度 ${scorePercent}%</span>` : ''}
            <span class="toggle-icon">▾</span>
          </span>
        </div>
        ${hasScore ? `
          <div class="convergence-bar">
            <div class="convergence-bar-fill" style="width: ${scorePercent}%">
            </div>
            <span class="convergence-label">${scorePercent}%</span>
          </div>
        ` : ''}
        <div class="mode-toggle">
          <button class="mode-toggle-btn active" onclick="this.parentElement.querySelector('.mode-toggle-btn.active')?.classList.remove('active');this.classList.add('active');this.closest('.viewpoints-card').querySelector('.viewpoints-body').dataset.mode='compact'">精简</button>
          <button class="mode-toggle-btn" onclick="this.parentElement.querySelector('.mode-toggle-btn.active')?.classList.remove('active');this.classList.add('active');this.closest('.viewpoints-card').querySelector('.viewpoints-body').dataset.mode='full'">全文</button>
        </div>
        <div class="viewpoints-body" data-mode="compact">
          <div class="viewpoints-grid">
            <div class="viewpoints-column">
              <h4>✅ 共识观点</h4>
              <ul>${renderViewpointList(consensus, 'consensus')}</ul>
            </div>
            <div class="viewpoints-column">
              <h4>⚡ 分歧观点</h4>
              <ul>${renderViewpointList(disagreement, 'disagreement')}</ul>
            </div>
          </div>
        </div>
      `;
      scrollToEnd();
    }

    function renderFinalSummary(summary) {
      if (!summary) return;
      const consensus = summary.consensus || summary.consensus_points || [];
      const disagreement = summary.disagreement || summary.disagreement_points || [];
      const verdict = summary.verdict ? `<div class="verdict-box"><span class="verdict-icon">📋</span><div><div style="font-weight:700;margin-bottom:8px;">结论</div><div class="markdown-content">${renderMarkdown(summary.verdict)}</div></div></div>` : '';
      $conclusionContent.innerHTML = `
        <div class="viewpoints-grid">
          <div class="viewpoints-column">
            <h4>✅ 最终共识</h4>
            <ul>${renderViewpointList(consensus, 'consensus')}</ul>
          </div>
          <div class="viewpoints-column">
            <h4>⚡ 保留分歧</h4>
            <ul>${renderViewpointList(disagreement, 'disagreement')}</ul>
          </div>
        </div>
        ${verdict}
      `;
      $conclusionCard.classList.remove('hidden');
      // 最终总结发光效果
      $conclusionCard.classList.add('final-summary-glow');
      scrollToEnd();
    }

    function mergeSpeech(speech, isNew = false) {
      if (!speech || speech.id === undefined || state.speechIdSet.has(speech.id)) return;
      state.speechIdSet.add(speech.id);
      state.speeches.push(speech);
      const streaming = state.streamSpeechMap.get(speech.id);
      if (streaming) {
        streaming.el.remove();
        state.streamSpeechMap.delete(speech.id);
      }
      renderSpeech(speech, isNew);
    }

    function renderSpeech(speech, isNew = false) {
      // Find role info
      let roleType = 'default';
      let roleName = '';
      if (speech.participant === 'coordinator') {
        roleType = 'coordinator';
        roleName = '👑 协调者';
      } else {
        const participantObj = state.participants.find(p => p.profile === speech.participant);
        if (participantObj) {
          roleType = getRoleType(participantObj.role);
          roleName = participantObj.role || '';
        }
      }

      const div = document.createElement('div');
      div.className = `speech-card role-${roleType}${isNew ? ' new highlight' : ''}`;
      div.id = `speech-${speech.id}`;

      const avatar = getParticipantAvatar(speech.participant);
      const speakerName = escapeHtml(speech.display_name || speech.participant);
      const safeRoleName = escapeHtml(roleName);
      const round = speech.round > 0 ? `<span class="round-badge" style="background: var(--rt-role-${roleType}-bg); color: var(--rt-role-${roleType})">R${speech.round}</span>` : '';
      const roleTagClass = getRoleTagClass(roleType);

      div.innerHTML = `
        <div class="flex items-start gap-3">
          <div class="speaker-avatar" style="background: var(--rt-role-${roleType}-bg); border-color: var(--rt-role-${roleType})" onclick="event.stopPropagation(); showAgentInfo('${escapeHtml(speech.participant)}', this)">${avatar}</div>
          <div class="flex-1 min-w-0">
            <div class="speech-header-meta">
              <span class="speaker-name font-semibold text-sm" style="color:var(--rt-text-primary)">${speakerName}</span>
              ${roleName ? `<span class="speaker-role-tag ${roleTagClass}">${safeRoleName}</span>` : ''}
              ${round}
              <span class="text-xs ml-auto" style="color:var(--rt-text-muted)">${formatTime(speech.created_at)}</span>
            </div>
            <div class="text-sm leading-relaxed markdown-content" style="color:var(--rt-text-secondary)">${renderMarkdown(speech.content)}</div>
          </div>
        </div>
      `;

      // Get or create round section
      getOrCreateRoundSection(speech.round, isNew);
      const prefix = activeSpeechesContainer ? activeSpeechesContainer.id : 'speechesContainer';
      const body = document.getElementById(`${prefix}-round-body-${speech.round}`);
      if (body) body.appendChild(div);

      // Update count
      const countEl = document.getElementById(`${prefix}-round-count-${speech.round}`);
      if (countEl && body) {
        const count = body.children.length;
        countEl.textContent = `${count} 条发言`;
      }

      // Remove highlight after 2s
      if (isNew) {
        setTimeout(() => div.classList.remove('highlight'), 2000);
        scrollToEnd();
      }
    }

    function renderConclusion(content) {
      $conclusionContent.innerHTML = `<div class="markdown-content">${renderMarkdown(content)}</div>`;
      $conclusionCard.classList.remove('hidden');
      setTimeout(() => {
        $conclusionCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 300);
      // Show replay entry when conclusion appears
      showReplayEntry();
    }

    function updateStatusUI() {
      const statusMap = {
        waiting: { cls: 'waiting', label: '等待中' },
        active:  { cls: 'live',    label: 'LIVE' },
        concluded: { cls: 'ended', label: '已结束' },
      };
      const info = statusMap[state.status] || statusMap.waiting;
      $statusBadge.className = `status-badge ${info.cls}`;
      $statusLabel.textContent = info.label;
      if (state.status === 'concluded') {
        $waitingState.classList.add('hidden');
        $activeState.classList.remove('hidden');
      }
    }

    function showRevoked() {
      $revokedState.classList.remove('hidden');
      if (eventSource) eventSource.close();
    }

    function setConnection(status) {
      $connDot.className = `conn-dot ${status}`;
      const labels = { connected: '已连接', disconnected: '已断开', reconnecting: '重连中…' };
      $connText.textContent = labels[status] || status;
    }

    // ---- Utils ----
    function escapeHtml(str) {
      const div = document.createElement('div');
      div.textContent = str;
      return div.innerHTML;
    }

    function formatTime(ts) {
      if (!ts) return '';
      const d = new Date(ts * 1000);
      return `${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`;
    }

    // ═══════════════════════════════════════
    // Share Interaction Logic
    // ═══════════════════════════════════════

    // DOM refs — Share
    const $shareContainer = document.getElementById('shareContainer');
    const $shareBtn = document.getElementById('shareBtn');
    const $sharePopover = document.getElementById('sharePopover');
    const $sharePanelContent = document.getElementById('sharePanelContent');
    const $shareLinkInput = document.getElementById('shareLinkInput');
    const $copyBtn = document.getElementById('copyBtn');
    const $revokeLinkBtn = document.getElementById('revokeLinkBtn');
    const $shareRevokedState = document.getElementById('shareRevokedState');
    const $mobileShareBtn = document.getElementById('mobileShareBtn');
    const $shareSheetOverlay = document.getElementById('shareSheetOverlay');
    const $shareSheet = document.getElementById('shareSheet');
    const $shareSheetContent = document.getElementById('shareSheetContent');
    const $shareSheetLinkInput = document.getElementById('shareSheetLinkInput');
    const $sheetCopyBtn = document.getElementById('sheetCopyBtn');
    const $sheetRevokeLinkBtn = document.getElementById('sheetRevokeLinkBtn');
    const $sheetRevokedState = document.getElementById('sheetRevokedState');
    const $revokeModalOverlay = document.getElementById('revokeModalOverlay');
    const $revokeCancelBtn = document.getElementById('revokeCancelBtn');
    const $revokeConfirmBtn = document.getElementById('revokeConfirmBtn');

    // State
    let shareLink = '';
    let popoverOpen = false;
    let sheetOpen = false;

    function isMobile() {
      return window.innerWidth < 768;
    }

    // ---- Share Button Click ----
    $shareBtn.addEventListener('click', async (e) => {
      e.stopPropagation();
      if (popoverOpen) {
        closePopover();
      } else {
        await openPopover();
      }
    });

    $mobileShareBtn.addEventListener('click', async () => {
      await openSheet();
    });

    // ---- Desktop Popover ----
    async function openPopover() {
      if (isMobile()) {
        await openSheet();
        return;
      }
      // Generate share link if not already set
      if (!shareLink) {
        await generateShareLink();
      }
      $sharePopover.classList.add('visible');
      popoverOpen = true;
    }

    function closePopover() {
      $sharePopover.classList.remove('visible');
      popoverOpen = false;
    }

    // Close popover on click outside
    document.addEventListener('click', (e) => {
      if (popoverOpen && !$shareContainer.contains(e.target)) {
        closePopover();
      }
    });

    // Close popover on ESC
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        if (revokeModalOpen) {
          closeRevokeModal();
        } else if (sheetOpen) {
          closeSheet();
        } else if (popoverOpen) {
          closePopover();
        }
      }
    });

    // ---- Mobile Bottom Sheet ----
    async function openSheet() {
      if (!shareLink) {
        await generateShareLink();
      }
      $shareSheetOverlay.classList.add('visible');
      $shareSheet.classList.add('visible');
      sheetOpen = true;
    }

    function closeSheet() {
      $shareSheetOverlay.classList.remove('visible');
      $shareSheet.classList.remove('visible');
      sheetOpen = false;
    }

    $shareSheetOverlay.addEventListener('click', closeSheet);

    // ---- Generate Share Link ----
    async function generateShareLink() {
      try {
        const resp = await fetch(`${API_BASE}/api/${CONFIG.token}/share`, {
          method: 'POST',
        });
        if (resp.ok) {
          const data = await resp.json();
          // Build full URL from the relative share_url
          shareLink = `${location.origin}${data.share_url}`;
        } else {
          // Fallback: just use current URL
          shareLink = location.href;
        }
      } catch {
        shareLink = location.href;
      }

      // Update UI
      $shareLinkInput.value = shareLink;
      $shareSheetLinkInput.value = shareLink;
    }

    // ---- Copy to Clipboard ----
    function copyToClipboard(text) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        return navigator.clipboard.writeText(text);
      }
      // Fallback for WeChat / old browsers
      return new Promise((resolve, reject) => {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.cssText = 'position:fixed;left:-9999px;top:-9999px;opacity:0';
        document.body.appendChild(textarea);
        textarea.select();
        try {
          document.execCommand('copy');
          resolve();
        } catch (err) {
          reject(err);
        } finally {
          document.body.removeChild(textarea);
        }
      });
    }

    function showCopySuccess(btn, originalText) {
      btn.textContent = '✓ 已复制';
      btn.classList.add('copied');
      btn.disabled = true;
      setTimeout(() => {
        btn.textContent = originalText;
        btn.classList.remove('copied');
        btn.disabled = false;
      }, 2000);
    }

    $copyBtn.addEventListener('click', async () => {
      if (!shareLink) return;
      try {
        await copyToClipboard(shareLink);
        showCopySuccess($copyBtn, '复制');
      } catch {
        // If clipboard fails, select the input so user can manually copy
        $shareLinkInput.select();
      }
    });

    $sheetCopyBtn.addEventListener('click', async () => {
      if (!shareLink) return;
      try {
        await copyToClipboard(shareLink);
        showCopySuccess($sheetCopyBtn, '复制链接');
      } catch {
        $shareSheetLinkInput.select();
      }
    });

    // ---- Revoke Confirmation Modal ----
    let revokeModalOpen = false;

    function openRevokeModal() {
      $revokeModalOverlay.classList.add('visible');
      revokeModalOpen = true;
    }

    function closeRevokeModal() {
      $revokeModalOverlay.classList.remove('visible');
      revokeModalOpen = false;
    }

    $revokeLinkBtn.addEventListener('click', () => {
      openRevokeModal();
    });

    $sheetRevokeLinkBtn.addEventListener('click', () => {
      openRevokeModal();
    });

    $revokeCancelBtn.addEventListener('click', closeRevokeModal);

    // Close modal on overlay click
    $revokeModalOverlay.addEventListener('click', (e) => {
      if (e.target === $revokeModalOverlay) {
        closeRevokeModal();
      }
    });

    // ---- Revoke Confirm ----
    $revokeConfirmBtn.addEventListener('click', async () => {
      $revokeConfirmBtn.disabled = true;
      $revokeConfirmBtn.textContent = '撤销中…';

      try {
        const resp = await fetch(`${API_BASE}/api/${CONFIG.token}/revoke`, {
          method: 'POST',
        });

        if (resp.ok) {
          closeRevokeModal();
          showRevokedInPanel();
          // The SSE 'revoked' event will show the full-page revoked state
        } else {
          alert('撤销失败，请重试');
          $revokeConfirmBtn.disabled = false;
          $revokeConfirmBtn.textContent = '确认撤销';
        }
      } catch {
        alert('网络错误，请重试');
        $revokeConfirmBtn.disabled = false;
        $revokeConfirmBtn.textContent = '确认撤销';
      }
    });

    function showRevokedInPanel() {
      // Desktop popover
      $sharePanelContent.classList.add('hidden');
      $shareRevokedState.classList.remove('hidden');
      // Mobile sheet
      $shareSheetContent.classList.add('hidden');
      $sheetRevokedState.classList.remove('hidden');
      // Auto-close panels after 3s
      setTimeout(() => {
        closePopover();
        closeSheet();
      }, 3000);
    }

    // ---- Sprint 3: 触摸交互优化 ----
    (function initTouchInteractions() {
      if (!('ontouchstart' in window)) return;  // 非触屏设备跳过

      let longPressTimer = null;
      let touchStartX = 0;
      let touchStartY = 0;
      let longPressTarget = null;

      // 长按发言卡片 → 弹出操作菜单（复制、分享）
      document.addEventListener('touchstart', function(e) {
        const card = e.target.closest('.speech-card');
        if (!card) return;

        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
        longPressTarget = card;

        longPressTimer = setTimeout(function() {
          if (!longPressTarget) return;
          const contentEl = longPressTarget.querySelector('.markdown-content');
          const text = contentEl ? contentEl.textContent : '';
          showTouchMenu(longPressTarget, text);
          longPressTarget = null;
        }, 600);
      }, { passive: true });

      document.addEventListener('touchmove', function(e) {
        if (!longPressTimer) return;
        const dx = Math.abs(e.touches[0].clientX - touchStartX);
        const dy = Math.abs(e.touches[0].clientY - touchStartY);
        if (dx > 10 || dy > 10) {
          clearTimeout(longPressTimer);
          longPressTimer = null;
        }
      }, { passive: true });

      document.addEventListener('touchend', function() {
        if (longPressTimer) {
          clearTimeout(longPressTimer);
          longPressTimer = null;
        }
      }, { passive: true });

      // 长按菜单
      function showTouchMenu(anchor, text) {
        closeTouchMenu();
        const rect = anchor.getBoundingClientRect();
        const menu = document.createElement('div');
        menu.className = 'touch-menu';
        menu.style.cssText = 'position:fixed;z-index:1200;background:rgba(15,23,42,0.97);border:1px solid var(--rt-border-light);border-radius:var(--rt-radius-md);padding:4px;box-shadow:0 8px 32px rgba(0,0,0,0.5);backdrop-filter:blur(12px);min-width:140px;animation:popIn 0.18s ease-out;';
        const top = Math.min(rect.top, window.innerHeight - 120);
        menu.style.top = top + 'px';
        menu.style.left = Math.max(8, Math.min(rect.left, window.innerWidth - 160)) + 'px';
        menu.innerHTML = '<button class="touch-menu-item" data-action="copy" style="display:block;width:100%;text-align:left;padding:10px 14px;border:none;background:none;color:var(--rt-text-primary);font-size:14px;cursor:pointer;border-radius:6px">📋 复制内容</button>';
        document.body.appendChild(menu);

        menu.querySelector('[data-action="copy"]').addEventListener('click', function() {
          navigator.clipboard.writeText(text).then(function() {
            showCopyToast();
          });
          closeTouchMenu();
        });

        setTimeout(function() {
          document.addEventListener('touchstart', onTouchOutside);
        }, 50);

        function onTouchOutside(e) {
          if (!menu.contains(e.target)) closeTouchMenu();
        }
        menu._outsideHandler = onTouchOutside;
      }

      function closeTouchMenu() {
        const menu = document.querySelector('.touch-menu');
        if (menu) {
          if (menu._outsideHandler) document.removeEventListener('touchstart', menu._outsideHandler);
          menu.remove();
        }
      }

      function showCopyToast() {
        const toast = document.createElement('div');
        toast.style.cssText = 'position:fixed;bottom:100px;left:50%;transform:translateX(-50%);background:rgba(34,197,94,0.9);color:#fff;padding:8px 20px;border-radius:999px;font-size:14px;z-index:1300;animation:fadeSlideIn 0.3s ease-out;';
        toast.textContent = '✓ 已复制';
        document.body.appendChild(toast);
        setTimeout(function() { toast.remove(); }, 1500);
      }

      // 双指下滑 → 快速回到顶部
      let lastTouchEnd = 0;
      document.addEventListener('touchend', function(e) {
        const now = Date.now();
        if (now - lastTouchEnd < 300) {
          // 双击 → 回到顶部
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        lastTouchEnd = now;
      }, { passive: true });
    })();

    // ---- Init ----
    
    // ═══════════════════════════════════════
    // Replay Player Core Logic (Sprint 2)
    // ═══════════════════════════════════════

    let replayState = {
      isPlaying: false,
      speed: 1,
      currentTimeMs: 0,
      totalDurationMs: 0,
      eventSource: null,
      events: [],
    };

    function formatDuration(ms) {
      const totalSec = Math.floor(ms / 1000);
      const m = Math.floor(totalSec / 60).toString().padStart(2, '0');
      const s = (totalSec % 60).toString().padStart(2, '0');
      return `${m}:${s}`;
    }

    function showReplayEntry() {
      const $replayEntry = document.getElementById('replayEntry');
      if (!$replayEntry) return;

      // Fetch meta to show in entry card
      fetch(`${API_BASE}/api/${CONFIG.token}/replay/meta`)
        .then(r => r.json())
        .then(data => {
          if (data.ok || data.duration !== undefined) {
            $replayEntry.classList.remove('hidden');
            const totalRounds = data.rounds ? data.rounds.length : 0;
            const totalEvents = data.totalEvents || 0;
            const durationStr = formatDuration(data.duration);
            document.getElementById('replayEntryMeta').textContent = 
              `${totalRounds} 轮讨论 · ${totalEvents} 段事件 · ${durationStr}`;
            
            // Render agent chips in entry card
            const $agentsContainer = document.getElementById('replayEntryAgents');
            if ($agentsContainer && data.agents) {
              $agentsContainer.innerHTML = data.agents.map(a => {
                const avatar = getParticipantAvatar(a.id);
                return `<span class="agent-chip" title="${escapeHtml(a.name)}">${avatar}</span>`;
              }).join('');
            }
          }
        })
        .catch(err => console.error("Error loading replay meta:", err));
    }

    // Enter Replay Mode
    window.enterReplayMode = function() {
      const $mainContent = document.getElementById('mainContent');
      const $replayView = document.getElementById('replayView');
      if (!$mainContent || !$replayView) return;

      $mainContent.classList.add('hidden');
      $replayView.classList.remove('hidden');
      document.body.classList.add('replay-mode');

      // Switch active speeches container
      activeSpeechesContainer = document.getElementById('replaySpeeches');
      activeSpeechesContainer.innerHTML = '';

      // Initialize replay controls
      initReplayPlayer();
    };

    // Exit Replay Mode
    window.exitReplayMode = function() {
      const $mainContent = document.getElementById('mainContent');
      const $replayView = document.getElementById('replayView');
      if (!$mainContent || !$replayView) return;

      stopReplay();

      $replayView.classList.add('hidden');
      $mainContent.classList.remove('hidden');
      document.body.classList.remove('replay-mode');

      activeSpeechesContainer = $speechesContainer;
    };

    function initReplayPlayer() {
      replayState.isPlaying = false;
      replayState.speed = 1;
      replayState.currentTimeMs = 0;
      updatePlayBtnUI();
      updateSpeedBtnUI();

      // Fetch meta
      fetch(`${API_BASE}/api/${CONFIG.token}/replay/meta`)
        .then(r => r.json())
        .then(data => {
          if (data.ok || data.duration !== undefined) {
            replayState.totalDurationMs = data.duration;
            document.getElementById('replayTotalTime').textContent = formatDuration(data.duration);
            document.getElementById('replayTopicTitle').textContent = state.topic || '回放';
            
            // Render timeline strip nodes
            const $timelineStrip = document.getElementById('timelineStrip');
            if ($timelineStrip && data.rounds) {
              let html = '';
              data.rounds.forEach((rnd, index) => {
                const pct = (rnd.offsetMs / data.duration) * 100;
                html += `
                  <div class="timeline-node round-marker" style="left: ${pct}%" onclick="seekReplay(${rnd.offsetMs})" title="第 ${rnd.round} 轮"></div>
                  ${index < data.rounds.length - 1 ? '<div class="timeline-connector"></div>' : ''}
                `;
              });
              $timelineStrip.innerHTML = html;
            }
          }
        });

      // Bind progress bar clicking/dragging
      const $track = document.getElementById('replayProgressTrack');
      if ($track) {
        $track.onclick = (e) => {
          const rect = $track.getBoundingClientRect();
          const pct = (e.clientX - rect.left) / rect.width;
          seekReplay(pct * replayState.totalDurationMs);
        };
      }

      // Bind control buttons
      const $playBtn = document.getElementById('replayPlayBtn');
      if ($playBtn) {
        $playBtn.onclick = togglePlayReplay;
      }

      // Bind speed buttons
      const bindSpeedBtns = (containerId) => {
        const container = document.getElementById(containerId);
        if (!container) return;
        container.querySelectorAll('.replay-speed-btn').forEach(btn => {
          btn.onclick = () => {
            const spd = parseFloat(btn.dataset.speed || '1');
            setReplaySpeed(spd);
          };
        });
      };
      bindSpeedBtns('replaySpeedSelector');
      bindSpeedBtns('replaySpeedSelectorBottom');
    }

    function updatePlayBtnUI() {
      const $playBtn = document.getElementById('replayPlayBtn');
      if ($playBtn) {
        $playBtn.textContent = replayState.isPlaying ? '⏸' : '▶';
      }
      if (replayState.isPlaying) {
        document.body.classList.remove('paused');
      } else {
        document.body.classList.add('paused');
      }
    }

    function updateSpeedBtnUI() {
      const setBtnActive = (containerId) => {
        const container = document.getElementById(containerId);
        if (!container) return;
        container.querySelectorAll('.replay-speed-btn').forEach(btn => {
          if (parseFloat(btn.dataset.speed) === replayState.speed) {
            btn.classList.add('active');
          } else {
            btn.classList.remove('active');
          }
        });
      };
      setBtnActive('replaySpeedSelector');
      setBtnActive('replaySpeedSelectorBottom');
    }

    function togglePlayReplay() {
      if (replayState.isPlaying) {
        pauseReplay();
      } else {
        playReplay();
      }
    }

    function playReplay() {
      if (replayState.isPlaying) return;
      replayState.isPlaying = true;
      updatePlayBtnUI();
      startReplayStream(replayState.currentTimeMs);
    }

    function pauseReplay() {
      if (!replayState.isPlaying) return;
      replayState.isPlaying = false;
      updatePlayBtnUI();
      if (replayState.eventSource) {
        replayState.eventSource.close();
        replayState.eventSource = null;
      }
    }

    function stopReplay() {
      pauseReplay();
      replayState.currentTimeMs = 0;
      updateProgressBar(0);
    }

    function setReplaySpeed(speed) {
      replayState.speed = speed;
      updateSpeedBtnUI();
      if (replayState.isPlaying) {
        pauseReplay();
        playReplay();
      }
    }

    window.seekReplay = function(timeMs) {
      replayState.currentTimeMs = Math.max(0, Math.min(timeMs, replayState.totalDurationMs));
      updateProgressBar(replayState.currentTimeMs);
      
      // Clear current replay speeches
      activeSpeechesContainer.innerHTML = '';
      
      if (replayState.isPlaying) {
        pauseReplay();
        playReplay();
      } else {
        fetchInstantReplayUpTo(replayState.currentTimeMs);
      }
    };

    function updateProgressBar(currentMs) {
      const pct = replayState.totalDurationMs ? (currentMs / replayState.totalDurationMs) * 100 : 0;
      const $fill = document.getElementById('replayProgressFill');
      const $handle = document.getElementById('replayProgressHandle');
      if ($fill) $fill.style.width = `${pct}%`;
      if ($handle) $handle.style.left = `${pct}%`;
      document.getElementById('replayCurrentTime').textContent = formatDuration(currentMs);
    }

    function startReplayStream(fromMs) {
      if (replayState.eventSource) replayState.eventSource.close();
      
      const url = `${API_BASE}/api/${CONFIG.token}/replay/stream?from=${Math.floor(fromMs)}&speed=${replayState.speed}`;
      replayState.eventSource = new EventSource(url);

      replayState.eventSource.addEventListener('replay_progress', (e) => {
        const data = JSON.parse(e.data);
        replayState.currentTimeMs = data.currentMs;
        updateProgressBar(data.currentMs);
        if (data.round !== undefined) {
          document.getElementById('replayRoundInfo').textContent = `第 ${data.round} 轮`;
        }
      });

      replayState.eventSource.addEventListener('replay_event', (e) => {
        const ev = JSON.parse(e.data);
        applyStreamEvent(ev);
      });

      replayState.eventSource.addEventListener('replay_end', () => {
        pauseReplay();
        replayState.currentTimeMs = replayState.totalDurationMs;
        updateProgressBar(replayState.totalDurationMs);
      });

      replayState.eventSource.onerror = () => {
        pauseReplay();
      };
    }

    function fetchInstantReplayUpTo(toMs) {
      if (replayState.eventSource) replayState.eventSource.close();
      activeSpeechesContainer.innerHTML = '';
      
      const url = `${API_BASE}/api/${CONFIG.token}/replay/stream?from=0&speed=0`;
      const es = new EventSource(url);
      
      es.addEventListener('replay_event', (e) => {
        const ev = JSON.parse(e.data);
        if (ev._offsetMs <= toMs) {
          applyStreamEvent(ev);
        }
      });
      
      es.addEventListener('replay_end', () => {
        es.close();
      });
      
      es.onerror = () => {
        es.close();
      };
    }

    connectSSE();