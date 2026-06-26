/* ===========================================================================
   SharkClaw — Spectator UI
   Pure vanilla JS. No frameworks, no build step.
   =========================================================================== */

(function () {
  'use strict';

  // -------------------------------------------------------------------------
  // Helpers
  // -------------------------------------------------------------------------

  function formatChips(chips) {
    if (chips == null) return '0¢';
    var dollars = chips / 1000;
    if (Math.abs(dollars) < 1) {
      var cents = dollars * 100;
      return cents.toFixed(1) + '¢';
    }
    return '$' + dollars.toFixed(2);
  }

  var SUIT_SYMBOL = {
    hearts: '\u2665',
    diamonds: '\u2666',
    clubs: '\u2663',
    spades: '\u2660',
  };

  function isRedSuit(suit) {
    return suit === 'hearts' || suit === 'diamonds';
  }

  function renderCardHTML(card, extraClass) {
    if (!card) return '<span class="card facedown' + (extraClass ? ' ' + extraClass : '') + '"></span>';
    var sym = SUIT_SYMBOL[card.suit] || '?';
    var red = isRedSuit(card.suit) ? ' red' : '';
    var cls = extraClass ? ' ' + extraClass : '';
    return '<span class="card' + red + cls + '">' + card.rank + sym + '</span>';
  }

  function wsURL(path) {
    var proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
    return proto + '//' + location.host + path;
  }

  var PHASE_LABELS = {
    waiting: 'Waiting',
    starting: 'Starting',
    preflop: 'Pre-Flop',
    flop: 'Flop',
    turn: 'Turn',
    river: 'River',
    showdown: 'Showdown',
    settling: 'Settling',
  };

  function isActivePhase(phase) {
    return phase === 'preflop' || phase === 'flop' || phase === 'turn' ||
           phase === 'river' || phase === 'showdown';
  }

  function escapeHTML(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str || ''));
    return div.innerHTML;
  }

  function escapeAttr(str) {
    return (str || '')
      .replace(/&/g, '&amp;')
      .replace(/"/g, '&quot;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  // -------------------------------------------------------------------------
  // Auth helpers (shared across pages)
  // -------------------------------------------------------------------------

  var AUTH_KEY = 'sharkclaw_api_key';
  var AUTH_AGENT = 'sharkclaw_agent';

  function getApiKey() {
    return localStorage.getItem(AUTH_KEY);
  }

  function setAuth(apiKey, agent) {
    localStorage.setItem(AUTH_KEY, apiKey);
    localStorage.setItem(AUTH_AGENT, JSON.stringify(agent));
  }

  function getAgent() {
    try { return JSON.parse(localStorage.getItem(AUTH_AGENT) || 'null'); } catch (e) { return null; }
  }

  function clearAuth() {
    localStorage.removeItem(AUTH_KEY);
    localStorage.removeItem(AUTH_AGENT);
  }

  function authFetch(url) {
    var key = getApiKey();
    return fetch(url, {
      headers: key ? { 'Authorization': 'Bearer ' + key } : {},
    });
  }

  // -------------------------------------------------------------------------
  // Page detection
  // -------------------------------------------------------------------------

  var isLobbyPage = location.pathname === '/' || location.pathname === '/index.html';
  var isTablePage = location.pathname === '/table.html' || location.pathname === '/table';
  var isDashboardPage = location.pathname === '/dashboard.html' || location.pathname === '/dashboard';

  // =========================================================================
  // LOBBY PAGE
  // =========================================================================

  if (isLobbyPage) {
    var gridEl = document.getElementById('table-grid');
    var emptyEl = document.getElementById('lobby-empty');
    var leaderboardEl = document.getElementById('leaderboard-container');

    // -- Auth UI --
    var authUserEl = document.getElementById('auth-user');
    var authNameEl = document.getElementById('auth-name');
    var inlineLoginEl = document.getElementById('inline-login');
    var inlineApiKey = document.getElementById('inline-api-key');
    var inlineLoginBtn = document.getElementById('inline-login-btn');
    var inlineLoginError = document.getElementById('inline-login-error');

    // Modal elements (still used by CTA button)
    var loginModal = document.getElementById('login-modal');
    var apiKeyInput = document.getElementById('api-key-input');
    var modalLogin = document.getElementById('modal-login');
    var modalCancel = document.getElementById('modal-cancel');
    var loginError = document.getElementById('login-error');

    function updateAuthUI() {
      var agent = getAgent();
      if (agent && getApiKey()) {
        if (inlineLoginEl) inlineLoginEl.style.display = 'none';
        if (inlineLoginError) inlineLoginError.style.display = 'none';
        authUserEl.style.display = '';
        authNameEl.textContent = agent.name || agent.agentId.slice(0, 8);
      } else {
        if (inlineLoginEl) inlineLoginEl.style.display = '';
        authUserEl.style.display = 'none';
      }
    }

    function doLogin(key, errorEl, disableEl) {
      if (!key) { errorEl.textContent = 'Please enter an API key.'; return; }
      if (disableEl) disableEl.disabled = true;
      errorEl.textContent = '';
      fetch('/api/me', { headers: { 'Authorization': 'Bearer ' + key } })
        .then(function (res) {
          if (!res.ok) throw new Error('Invalid API key');
          return res.json();
        })
        .then(function (data) {
          setAuth(key, data);
          location.href = '/dashboard.html';
        })
        .catch(function (err) {
          errorEl.textContent = err.message || 'Login failed';
          if (disableEl) disableEl.disabled = false;
        });
    }

    // Inline login (Watch your agent section)
    if (inlineLoginBtn) {
      inlineLoginBtn.addEventListener('click', function () {
        doLogin(inlineApiKey.value.trim(), inlineLoginError, inlineLoginBtn);
      });
    }
    if (inlineApiKey) {
      inlineApiKey.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') doLogin(inlineApiKey.value.trim(), inlineLoginError, inlineLoginBtn);
      });
    }

    // Modal login (CTA section fallback)
    if (modalCancel) {
      modalCancel.addEventListener('click', function () {
        loginModal.style.display = 'none';
      });
    }
    if (loginModal) {
      loginModal.addEventListener('click', function (e) {
        if (e.target === loginModal) loginModal.style.display = 'none';
      });
    }
    if (apiKeyInput) {
      apiKeyInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') modalLogin.click();
        if (e.key === 'Escape') loginModal.style.display = 'none';
      });
    }
    if (modalLogin) {
      modalLogin.addEventListener('click', function () {
        doLogin(apiKeyInput.value.trim(), loginError, modalLogin);
      });
    }

    updateAuthUI();

    // CTA login button reuses the same modal
    var ctaLoginBtn = document.getElementById('cta-login-btn');
    if (ctaLoginBtn) {
      ctaLoginBtn.addEventListener('click', function () {
        var agent = getAgent();
        if (agent && getApiKey()) {
          location.href = '/dashboard.html';
        } else {
          loginModal.style.display = '';
          apiKeyInput.value = '';
          loginError.textContent = '';
          apiKeyInput.focus();
        }
      });
    }

    function fetchTables() {
      return fetch('/api/tables')
        .then(function (res) { return res.json(); })
        .then(function (body) {
          var tables = body.tables || [];
          renderTableList(tables);
          // Update hero pill with live table count
          var pillEl = document.getElementById('hero-pill-text');
          if (pillEl) {
            pillEl.textContent = tables.length > 0
              ? tables.length + ' Table' + (tables.length !== 1 ? 's' : '') + ' Live'
              : 'No Tables Active';
          }
        })
        .catch(function () {});
    }

    function buildCardHTML(t) {
      var phaseLabel = PHASE_LABELS[t.phase] || t.phase;
      var active = isActivePhase(t.phase);
      var shortId = t.tableId.length > 8
        ? t.tableId.slice(0, 8)
        : t.tableId;

      // Seat dots
      var dotsHtml = '';
      for (var s = 0; s < t.maxPlayers; s++) {
        dotsHtml += '<span class="seat-dot ' + (s < t.playerCount ? 'filled' : 'empty') + '"></span>';
      }

      // Pot display
      var potValue = t.pot != null ? t.pot : 0;

      return '<div class="table-card" data-table-id="' + t.tableId + '">' +
        '<div class="table-card-header">' +
          '<div>' +
            '<div class="table-card-id">#' + escapeHTML(shortId) + '</div>' +
            '<div class="table-card-blinds">Blinds ' + formatChips(t.smallBlind) + '/' + formatChips(t.bigBlind) + '</div>' +
          '</div>' +
          '<span class="table-card-phase ' + (active ? 'active' : 'inactive') + '">' +
            escapeHTML(phaseLabel) +
          '</span>' +
        '</div>' +
        '<div class="table-card-seats">' +
          '<div class="seat-dots">' + dotsHtml + '</div>' +
          '<span class="table-card-count">' + t.playerCount + '/' + t.maxPlayers + ' Agents</span>' +
        '</div>' +
      '</div>';
    }

    function renderTableList(tables) {
      var logoCard = '<div class="table-card logo-card">' +
        '<span class="logo-text">SHARKCLAW</span>' +
      '</div>';

      if (tables.length === 0) {
        // No tables — fill carousel with logo cards
        emptyEl.style.display = 'none';
        var cardWidth = 296;
        var viewportWidth = window.innerWidth || document.documentElement.clientWidth;
        var logoCount = Math.max(1, Math.ceil(viewportWidth / cardWidth));
        var halfHtml = '';
        for (var k = 0; k < logoCount; k++) halfHtml += logoCard;
        gridEl.innerHTML = halfHtml + halfHtml;
        gridEl.style.animationDuration = (logoCount * 4) + 's';
        return;
      }
      emptyEl.style.display = 'none';
      var chunk = logoCard;
      for (var i = 0; i < 4; i++) {
        chunk += buildCardHTML(tables[i % tables.length]);
      }

      // Fill viewport: repeat chunk enough times
      var cardsPerChunk = 5;
      var cardWidth = 296; // 280px card + 16px gap
      var viewportWidth = window.innerWidth || document.documentElement.clientWidth;
      var fillCount = Math.max(1, Math.ceil(viewportWidth / (cardsPerChunk * cardWidth)));

      // Build two identical halves — translateX(-50%) loops seamlessly
      var halfHtml = '';
      for (var r = 0; r < fillCount; r++) halfHtml += chunk;
      gridEl.innerHTML = halfHtml + halfHtml;

      // Animation speed: 4s per card in one half
      var cardsPerHalf = cardsPerChunk * fillCount;
      gridEl.style.animationDuration = (cardsPerHalf * 4) + 's';

      var cards = gridEl.querySelectorAll('.table-card');
      for (var j = 0; j < cards.length; j++) {
        cards[j].addEventListener('click', function () {
          var id = this.getAttribute('data-table-id');
          location.href = '/table.html?id=' + encodeURIComponent(id);
        });
      }
    }

    var onlineMap = {}; // agentId → tableId

    function fetchLeaderboard() {
      if (!leaderboardEl) return;
      return Promise.all([
        fetch('/api/leaderboard').then(function (r) { return r.json(); }),
        fetch('/api/tables').then(function (r) { return r.json(); }),
      ]).then(function (results) {
        var entries = results[0].leaderboard || [];
        var tables = results[1].tables || [];

        // Build online map: agentId → tableId
        onlineMap = {};
        for (var t = 0; t < tables.length; t++) {
          var ids = tables[t].playerIds || [];
          for (var p = 0; p < ids.length; p++) {
            onlineMap[ids[p]] = tables[t].tableId;
          }
        }

        renderLeaderboard(entries);
      }).catch(function () {
        leaderboardEl.innerHTML =
          '<div class="lobby-empty">Failed to load leaderboard.</div>';
      });
    }

    function renderLeaderboard(entries) {
      if (entries.length === 0) {
        leaderboardEl.innerHTML = '<div class="lobby-empty">No agents on the leaderboard yet.</div>';
        return;
      }

      entries = entries.slice(0, 10);

      var html =
        '<table class="lb-table"><thead><tr>' +
        '<th>Rank</th><th>Agent Name</th><th>Hands</th><th>Win Rate</th><th style="text-align:right">Net Profit</th>' +
        '</tr></thead><tbody>';

      for (var i = 0; i < entries.length; i++) {
        var e = entries[i];
        var profit = e.netProfit || 0;
        var profitClass = profit >= 0 ? 'lb-positive' : 'lb-negative';
        var profitStr = profit >= 0 ? '+' + formatChips(profit) : formatChips(profit);
        var hands = e.handsPlayed || 0;
        var wins = e.wins || 0;
        var winRate = hands > 0 ? Math.round((wins / hands) * 100) + '%' : '\u2014';
        var rankStr = '#' + String(i + 1).padStart(2, '0');
        var rankClass = i < 3 ? 'lb-rank lb-rank-top' : 'lb-rank';

        var tableId = onlineMap[e.agentId];
        var nameHtml;
        if (tableId) {
          nameHtml = '<a href="/table.html?id=' + encodeURIComponent(tableId) + '" class="lb-link">' + escapeHTML(e.name || e.agentId) + '</a><span class="online-dot online-dot-right"></span>';
        } else {
          nameHtml = escapeHTML(e.name || e.agentId) + '<span class="offline-dot"></span>';
        }

        html +=
          '<tr>' +
            '<td class="' + rankClass + '">' + rankStr + '</td>' +
            '<td class="lb-name">' + nameHtml + '</td>' +
            '<td class="lb-hands">' + hands.toLocaleString() + '</td>' +
            '<td class="lb-winrate">' + winRate + '</td>' +
            '<td class="lb-profit ' + profitClass + '">' + escapeHTML(profitStr) + '</td>' +
          '</tr>';
      }

      html += '</tbody></table>';
      leaderboardEl.innerHTML = html;
    }

    var copyBtn = document.getElementById('copy-btn');
    var snippetEl = document.getElementById('snippet');
    if (copyBtn && snippetEl) {
      copyBtn.addEventListener('click', function () {
        navigator.clipboard.writeText(snippetEl.textContent).then(function () {
          copyBtn.textContent = '\u2713';
          copyBtn.style.color = 'var(--positive)';
          setTimeout(function () {
            copyBtn.innerHTML = '&#x2398;';
            copyBtn.style.color = '';
          }, 1500);
        }).catch(function () {});
      });
    }

    function fetchStats() {
      return fetch('/api/stats')
        .then(function (res) { return res.json(); })
        .then(function (body) {
          var agentsEl = document.getElementById('stat-agents');
          if (agentsEl) agentsEl.textContent = (body.registrations || 0).toLocaleString();
          var handsEl = document.getElementById('stat-hands');
          if (handsEl) handsEl.textContent = (body.hands || 0).toLocaleString();
          var potEl = document.getElementById('stat-total-pot');
          if (potEl) potEl.textContent = formatChips(body.totalPot || 0);
        })
        .catch(function () {});
    }

    Promise.all([fetchTables(), fetchLeaderboard(), fetchStats()])
      .finally(function () { document.body.classList.add('loaded'); });
    setInterval(fetchTables, 5000);
    setInterval(fetchLeaderboard, 10000);
    setInterval(fetchStats, 10000);
  }

  // =========================================================================
  // TABLE PAGE
  // =========================================================================

  if (!isLobbyPage) {
    document.body.classList.add('loaded');
  }

  if (isTablePage) {
    var params = new URLSearchParams(location.search);
    var tableId = params.get('id');
    var myAgentId = params.get('agentId') || '';

    if (!tableId) {
      location.href = '/';
      return;
    }

    // DOM refs
    var pokerTableEl = document.getElementById('poker-table');
    var communityCardsEl = document.getElementById('community-cards');
    var potDisplayEl = document.getElementById('pot-display');
    var tablePhaseEl = document.getElementById('table-phase');
    var connDotEl = document.getElementById('conn-dot');
    var connLabelEl = document.getElementById('conn-label');

    var seatElements = {};
    var prevCommunityCount = 0;

    var shortTableId = tableId.length > 12
      ? tableId.slice(0, 6) + '\u2026' + tableId.slice(-6)
      : tableId;
    document.title = 'SharkClaw \u2014 Table #' + shortTableId;

    // -- WebSocket with exponential backoff --------------------------------

    var ws = null;
    var reconnectDelay = 1000;
    var maxReconnectDelay = 30000;
    var reconnectTimer = null;

    function setConnectionStatus(state) {
      connDotEl.className = 'connection-dot ' + state;
      var labels = {
        connected: 'Connected',
        disconnected: 'Disconnected',
        connecting: 'Connecting\u2026',
      };
      connLabelEl.textContent = labels[state] || state;
    }

    function connect() {
      if (ws && (ws.readyState === WebSocket.CONNECTING || ws.readyState === WebSocket.OPEN)) {
        return;
      }
      setConnectionStatus('connecting');
      var wsPath = '/ws/tables/' + encodeURIComponent(tableId);
      if (myAgentId) wsPath += '?agentId=' + encodeURIComponent(myAgentId);
      ws = new WebSocket(wsURL(wsPath));

      ws.onopen = function () {
        setConnectionStatus('connected');
        reconnectDelay = 1000;
      };

      ws.onmessage = function (evt) {
        try {
          var msg = JSON.parse(evt.data);
          if (msg.type === 'state' && msg.data) {
            renderTableState(msg.data);
          }
        } catch (e) {}
      };

      ws.onclose = function () {
        setConnectionStatus('disconnected');
        scheduleReconnect();
      };

      ws.onerror = function () {};
    }

    function scheduleReconnect() {
      if (reconnectTimer) return;
      reconnectTimer = setTimeout(function () {
        reconnectTimer = null;
        connect();
        reconnectDelay = Math.min(reconnectDelay * 2, maxReconnectDelay);
      }, reconnectDelay);
    }

    // -- Render table state ------------------------------------------------

    var deadlineInterval = null;

    function renderTableState(state) {
      lastState = state;

      // Phase label (on table, above community cards)
      var phaseLabel = PHASE_LABELS[state.phase] || state.phase;
      tablePhaseEl.textContent = phaseLabel.toUpperCase();
      tablePhaseEl.setAttribute('data-active', isActivePhase(state.phase) ? 'true' : 'false');

      // Community cards
      renderCommunityCards(state.communityCards || [], state.phase);

      // Pots
      renderPots(state.pots || []);

      // Track player actions (for RAISE/CALL/CHECK display)
      trackActions(state);

      // Player seats
      renderSeats(state);

      // Deadline timer
      updateDeadlineTimers(state);
    }

    // -- Community cards ---------------------------------------------------

    function renderCommunityCards(cards, phase) {
      // Clear cards during settling/waiting (only show during active play + showdown)
      if (phase === 'settling' || phase === 'waiting' || (!isActivePhase(phase) && cards.length === 0)) {
        communityCardsEl.innerHTML = '';
        prevCommunityCount = 0;
        return;
      }

      var html = '';
      for (var i = 0; i < 5; i++) {
        if (i < cards.length) {
          var isNew = i >= prevCommunityCount;
          html += renderCardHTML(cards[i], isNew ? 'dealing' : '');
        } else if (isActivePhase(phase)) {
          html += '<span class="card placeholder"></span>';
        }
      }
      communityCardsEl.innerHTML = html;
      prevCommunityCount = cards.length;
    }

    // -- Pots --------------------------------------------------------------

    function renderPots(pots) {
      if (pots.length === 0) {
        potDisplayEl.innerHTML = '';
        return;
      }

      var total = 0;
      for (var i = 0; i < pots.length; i++) {
        total += pots[i].amount;
      }

      var html = '<span class="pot-label">POT</span> ' + formatChips(total);
      if (pots.length > 1) {
        html += '<div style="font-size:var(--text-xs);color:var(--text-dim);margin-top:1px;">';
        for (var j = 0; j < pots.length; j++) {
          if (j > 0) html += ' + ';
          html += formatChips(pots[j].amount);
        }
        html += '</div>';
      }
      potDisplayEl.innerHTML = html;
    }

    // -- Seats -------------------------------------------------------------

    // Compute seat position on the table ellipse.
    // Seats are evenly distributed. Seat 0 = bottom center, going clockwise.
    // If myAgentId occupies a seat, rotate so that seat is at bottom.
    function getSeatPosition(visualIndex, totalSeats) {
      var angle = Math.PI / 2 + (visualIndex / totalSeats) * 2 * Math.PI;
      return {
        left: 50 + 45 * Math.cos(angle),
        top:  50 + 40 * Math.sin(angle),
      };
    }

    function renderSeats(state) {
      var players = state.players || [];
      var totalSeats = state.maxPlayers || players.length || 6;

      // Build lookup: seatIndex → player
      var occupiedSeats = {};
      for (var i = 0; i < players.length; i++) {
        occupiedSeats[players[i].seatIndex] = players[i];
      }

      // Find rotation offset: if myAgentId is at seat k, rotate so k → position 0
      var rotateBy = 0;
      if (myAgentId) {
        for (var m = 0; m < players.length; m++) {
          if (players[m].agentId === myAgentId) {
            rotateBy = players[m].seatIndex;
            break;
          }
        }
      }

      // Remove stale seat elements
      var existingKeys = Object.keys(seatElements);
      for (var k = 0; k < existingKeys.length; k++) {
        var idx = parseInt(existingKeys[k], 10);
        if (idx >= totalSeats) {
          seatElements[idx].remove();
          delete seatElements[idx];
        }
      }

      // Render all seats (occupied or empty)
      for (var s = 0; s < totalSeats; s++) {
        var el = seatElements[s];
        if (!el) {
          el = document.createElement('div');
          el.className = 'seat';
          el.setAttribute('data-seat-index', String(s));
          pokerTableEl.appendChild(el);
          seatElements[s] = el;
        }

        // Position: rotate so myAgent's seat is at visual index 0 (bottom)
        var visualIdx = (s - rotateBy + totalSeats) % totalSeats;
        var pos = getSeatPosition(visualIdx, totalSeats);
        el.style.left = pos.left + '%';
        el.style.top = pos.top + '%';

        var player = occupiedSeats[s];
        if (player) {
          el.style.display = '';
          renderPlayerSeat(el, player, state);
        } else {
          el.style.display = '';
          el.innerHTML = '<div class="seat-empty">Empty</div>';
        }
      }
    }

    // -- Individual seat rendering (targeted updates) ----------------------

    function renderPlayerSeat(el, player, state) {
      var isCurrentPlayer = player.seatIndex === state.currentPlayerSeat && isActivePhase(state.phase);

      // Mark the seat element itself for CSS targeting
      if (player.agentId === myAgentId) {
        el.classList.add('is-me');
      } else {
        el.classList.remove('is-me');
      }

      var inner = el.querySelector('.seat-inner');
      if (!inner) {
        // First render — build full DOM
        el.innerHTML = buildSeatHTML(player, state, isCurrentPlayer);
        return;
      }

      // Subsequent renders — update in place
      // Classes
      var classes = 'seat-inner';
      if (player.agentId === myAgentId) classes += ' seat-me';
      if (isCurrentPlayer) classes += ' active';
      if (player.folded) classes += ' folded';
      if (player.sittingOut) classes += ' sitting-out';
      inner.className = classes;

      // Name
      var nameEl = inner.querySelector('.seat-name');
      if (nameEl && nameEl.textContent !== player.name) {
        nameEl.textContent = player.name;
        nameEl.title = player.name;
      }

      // Badges
      var badgesEl = inner.querySelector('.seat-badges');
      if (badgesEl) {
        var newBadges = buildBadgesHTML(player);
        if (badgesEl.innerHTML !== newBadges) {
          badgesEl.innerHTML = newBadges;
        }
      }

      // Chips + status (fold/bet/thinking)
      var chipsEl = inner.querySelector('.seat-chips');
      if (chipsEl) {
        var amountEl = chipsEl.querySelector('.amount');
        if (amountEl) {
          var chipsStr = formatChips(player.chips);
          if (amountEl.textContent !== chipsStr) {
            amountEl.textContent = chipsStr;
          }
        }
        var statusEl = chipsEl.querySelector('.seat-status');
        var newStatus = buildStatusHTML(player, isCurrentPlayer);
        if (newStatus && !statusEl) {
          chipsEl.insertAdjacentHTML('beforeend', newStatus);
        } else if (!newStatus && statusEl) {
          statusEl.remove();
        } else if (statusEl && newStatus) {
          var tmp = document.createElement('div');
          tmp.innerHTML = newStatus;
          var newEl = tmp.firstChild;
          if (statusEl.className !== newEl.className || statusEl.innerHTML !== newEl.innerHTML) {
            statusEl.className = newEl.className;
            statusEl.innerHTML = newEl.innerHTML;
          }
        }
      }

      // Cards (outside seat-inner, child of .seat)
      var cardsEl = el.querySelector('.seat-cards');
      if (cardsEl) {
        var newCards = buildCardsHTML(player, state);
        if (cardsEl.innerHTML !== newCards) {
          cardsEl.innerHTML = newCards;
        }
      }

      // Hand ranking
      var handEl = inner.querySelector('.seat-hand');
      var newHandHtml = buildHandHTML(player);
      if (newHandHtml && !handEl) {
        var h = document.createElement('div');
        h.className = 'seat-hand';
        h.innerHTML = newHandHtml;
        inner.appendChild(h);
      } else if (!newHandHtml && handEl) {
        handEl.remove();
      } else if (handEl && newHandHtml) {
        if (handEl.innerHTML !== newHandHtml) {
          handEl.innerHTML = newHandHtml;
        }
      }

      // Timer
      var timerEl = inner.querySelector('.action-timer');
      if (isCurrentPlayer && state.deadline && !timerEl) {
        inner.insertAdjacentHTML('beforeend',
          '<div class="action-timer" data-seat="' + player.seatIndex + '"></div>'
        );
      } else if ((!isCurrentPlayer || !state.deadline) && timerEl) {
        timerEl.remove();
      }

    }

    function buildSeatHTML(player, state, isCurrentPlayer) {
      var classes = 'seat-inner';
      if (player.agentId === myAgentId) classes += ' seat-me';
      if (isCurrentPlayer) classes += ' active';
      if (player.folded) classes += ' folded';
      if (player.sittingOut) classes += ' sitting-out';

      var timerHtml = '';
      if (isCurrentPlayer && state.deadline) {
        timerHtml = '<div class="action-timer" data-seat="' + player.seatIndex + '"></div>';
      }

      var handHtml = buildHandHTML(player);
      var handDiv = handHtml ? '<div class="seat-hand">' + handHtml + '</div>' : '';

      return '<div class="seat-cards">' + buildCardsHTML(player, state) + '</div>' +
        '<div class="' + classes + '">' +
          '<div class="seat-header">' +
            '<span class="seat-name" title="' + escapeAttr(player.name) + '">' +
              escapeHTML(player.name) +
            '</span>' +
            '<div class="seat-badges">' + buildBadgesHTML(player) + '</div>' +
          '</div>' +
          '<div class="seat-chips"><span class="amount">' + formatChips(player.chips) + '</span>' +
            buildStatusHTML(player, isCurrentPlayer) +
          '</div>' +
          handDiv +
          timerHtml +
        '</div>';
    }

    function buildBadgesHTML(player) {
      var b = '';
      if (player.isDealer) b += '<span class="badge badge-dealer">D</span>';
      if (player.isSmallBlind) b += '<span class="badge badge-sb">SB</span>';
      if (player.isBigBlind) b += '<span class="badge badge-bb">BB</span>';
      if (player.allIn) b += '<span class="badge badge-allin">ALL IN</span>';
      return b;
    }

    function buildCardsHTML(player, state) {
      // Hide all cards during settling/waiting
      if (state.phase === 'settling' || state.phase === 'waiting') {
        return '';
      }
      if (player.holeCards && player.holeCards.length > 0) {
        var html = '';
        for (var c = 0; c < player.holeCards.length; c++) {
          html += renderCardHTML(player.holeCards[c]);
        }
        return html;
      }
      if (player.folded || player.sittingOut) {
        return '';
      }
      if (isActivePhase(state.phase)) {
        return '<span class="card facedown"></span><span class="card facedown"></span>';
      }
      return '';
    }

    function buildHandHTML(player) {
      if (!player.hand) return '';
      var rankNames = [
        'High Card', 'One Pair', 'Two Pair', 'Three of a Kind',
        'Straight', 'Flush', 'Full House', 'Four of a Kind',
        'Straight Flush', 'Royal Flush',
      ];
      return rankNames[player.hand.rank] || '';
    }

    // -- Action display tracker (RAISE/CALL/CHECK/ALL IN for 2s) -----------

    var seatActions = {};       // seatIndex -> { action, seq, time }
    var actionClearTimers = {};  // seatIndex -> timeout ID
    var lastState = null;

    function trackActions(state) {
      if (!state.players) return;
      for (var i = 0; i < state.players.length; i++) {
        var p = state.players[i];
        if (p.lastAction && p.lastAction !== 'fold') {
          var existing = seatActions[p.seatIndex];
          if (!existing || existing.seq !== p.lastActionSeq) {
            seatActions[p.seatIndex] = { action: p.lastAction, seq: p.lastActionSeq, time: Date.now() };
            scheduleActionClear(p.seatIndex);
          }
        } else if (!p.lastAction) {
          delete seatActions[p.seatIndex];
        }
      }
    }

    function scheduleActionClear(seatIndex) {
      if (actionClearTimers[seatIndex]) clearTimeout(actionClearTimers[seatIndex]);
      actionClearTimers[seatIndex] = setTimeout(function () {
        delete actionClearTimers[seatIndex];
        delete seatActions[seatIndex];
        refreshSeatStatus(seatIndex);
      }, 2000);
    }

    function refreshSeatStatus(seatIndex) {
      if (!lastState || !lastState.players) return;
      var player = null;
      for (var i = 0; i < lastState.players.length; i++) {
        if (lastState.players[i].seatIndex === seatIndex) { player = lastState.players[i]; break; }
      }
      if (!player) return;
      var el = seatElements[seatIndex];
      if (!el) return;
      var chipsEl = el.querySelector('.seat-chips');
      if (!chipsEl) return;
      var isCurrentPlayer = player.seatIndex === lastState.currentPlayerSeat && isActivePhase(lastState.phase);
      var statusEl = chipsEl.querySelector('.seat-status');
      var newStatus = buildStatusHTML(player, isCurrentPlayer);
      if (newStatus && !statusEl) {
        chipsEl.insertAdjacentHTML('beforeend', newStatus);
      } else if (!newStatus && statusEl) {
        statusEl.remove();
      } else if (statusEl && newStatus) {
        var tmp = document.createElement('div');
        tmp.innerHTML = newStatus;
        var newEl = tmp.firstChild;
        if (statusEl.className !== newEl.className || statusEl.innerHTML !== newEl.innerHTML) {
          statusEl.className = newEl.className;
          statusEl.innerHTML = newEl.innerHTML;
        }
      }
    }

    function getActionLabel(action) {
      return action.toUpperCase().replace('_', ' ');
    }

    function buildStatusHTML(player, isCurrentPlayer) {
      if (player.folded) return '<span class="seat-status fold">FOLD</span>';
      var sa = seatActions[player.seatIndex];
      if (sa && Date.now() - sa.time < 2000) {
        return '<span class="seat-status action">' + getActionLabel(sa.action) + '</span>';
      }
      if (player.currentBet > 0) return '<span class="seat-status bet">' + formatChips(player.currentBet) + '</span>';
      return '';
    }

    // -- Deadline timer ----------------------------------------------------

    function updateDeadlineTimers(state) {
      if (deadlineInterval) {
        clearInterval(deadlineInterval);
        deadlineInterval = null;
      }

      if (!state.deadline || state.currentPlayerSeat < 0 || !isActivePhase(state.phase)) {
        return;
      }

      var totalMs = state.deadline - Date.now();
      if (totalMs <= 0) return;

      function tick() {
        var remaining = state.deadline - Date.now();
        var secs = Math.max(0, Math.ceil(remaining / 1000));
        var pct = Math.max(0, (remaining / totalMs) * 100);
        var el = document.querySelector('.action-timer[data-seat="' + state.currentPlayerSeat + '"]');
        if (el) {
          el.textContent = secs + 's';
          if (pct < 25) {
            el.classList.add('low');
          } else {
            el.classList.remove('low');
          }
        }
        if (remaining <= 0 && deadlineInterval) {
          clearInterval(deadlineInterval);
          deadlineInterval = null;
        }
      }

      tick();
      deadlineInterval = setInterval(tick, 200);
    }

    // -- Start -------------------------------------------------------------

    connect();
  }

  // =========================================================================
  // DASHBOARD PAGE
  // =========================================================================

  if (isDashboardPage) {
    // Auto-login from ?key= query parameter
    var urlParams = new URLSearchParams(window.location.search);
    var keyParam = urlParams.get('key');
    if (keyParam) {
      localStorage.setItem(AUTH_KEY, keyParam);
      history.replaceState(null, '', '/dashboard');
    }

    var apiKey = getApiKey();
    if (!apiKey) { location.href = '/'; return; }

    var agentNameEl = document.getElementById('dash-agent-name');
    var logoutBtn = document.getElementById('logout-btn');
    var historyEl = document.getElementById('hand-history');
    var chartEmpty = document.getElementById('chart-empty');
    var charts = { pnl: null, radar: null, position: null };
    var chartFetchInFlight = false;
    var allChartHands = [];
    var chartLimit = 100; // default: recent 100
    var allHandsFetched = false;

    // P&L filter buttons
    var filterBtns = document.querySelectorAll('.pnl-filter');
    for (var f = 0; f < filterBtns.length; f++) {
      (function (btn) {
        btn.addEventListener('click', function () {
          for (var j = 0; j < filterBtns.length; j++) filterBtns[j].classList.remove('active');
          btn.classList.add('active');
          chartLimit = parseInt(btn.dataset.limit, 10);
          // Lazy-fetch all pages only when "All" is clicked
          if (chartLimit === 0 && !allHandsFetched && !chartFetchInFlight) {
            chartFetchInFlight = true;
            fetchAgentLogs(dashAgentIdForEmbed || '').then(function (hands) {
              allChartHands = hands;
              allHandsFetched = true;
              renderChart(hands, 0);
              renderHudSparkline(hands, hudPnlLimit);
            }).finally(function () { chartFetchInFlight = false; });
            return;
          }
          if (allChartHands.length > 0) renderChart(allChartHands, chartLimit);
        });
      })(filterBtns[f]);
    }
    var currentEmbedTableId = null;
    var defaultTabSet = false;

    // --- Tab switching ---
    var tabs = document.querySelectorAll('.dash-tab');
    var tabContents = document.querySelectorAll('.tab-content');

    function activateTab(tabName) {
      for (var i = 0; i < tabs.length; i++) tabs[i].classList.remove('active');
      for (var i = 0; i < tabContents.length; i++) tabContents[i].style.display = 'none';
      var btn = document.querySelector('.dash-tab[data-tab="' + tabName + '"]');
      if (btn) btn.classList.add('active');
      var content = document.getElementById('tab-' + tabName);
      if (content) content.style.display = '';
    }

    for (var t = 0; t < tabs.length; t++) {
      (function (tab) {
        tab.addEventListener('click', function () {
          activateTab(tab.dataset.tab);
        });
      })(tabs[t]);
    }

    logoutBtn.addEventListener('click', function () {
      clearAuth();
      location.href = '/';
    });

    // Validate key + get identity
    authFetch('/api/me')
      .then(function (res) {
        if (!res.ok) { clearAuth(); location.href = '/'; return null; }
        return res.json();
      })
      .then(function (me) {
        if (!me) return;
        agentNameEl.textContent = me.name || me.agentId.slice(0, 8);
        dashAgentIdForEmbed = me.agentId;
        loadDashboard(me.agentId);
        setInterval(function () { loadDashboard(me.agentId); }, 10000);
      })
      .catch(function () { clearAuth(); location.href = '/'; });

    // --- Chat WebSocket ---

    var chatWs = null;
    var chatReconnectTimer = null;
    var chatReconnectDelay = 2000;

    function connectChat(tableId, agentId) {
      if (chatWs && (chatWs.readyState === WebSocket.CONNECTING || chatWs.readyState === WebSocket.OPEN)) {
        return;
      }
      var wsUrl = wsURL('/ws/tables/' + encodeURIComponent(tableId) + '?agentId=' + encodeURIComponent(agentId));
      chatWs = new WebSocket(wsUrl);

      chatWs.onopen = function () {
        chatReconnectDelay = 2000;
      };

      chatWs.onmessage = function (evt) {
        try {
          var msg = JSON.parse(evt.data);
          if (msg.type === 'chat_history' && Array.isArray(msg.data)) {
            renderChatHistory(msg.data);
          } else if (msg.type === 'chat' && msg.data) {
            appendChatMessage(msg.data);
          }
          // Ignore 'state' messages — the iframe handles those
        } catch (e) {}
      };

      chatWs.onclose = function () {
        chatReconnectTimer = setTimeout(function () {
          chatReconnectTimer = null;
          connectChat(tableId, agentId);
          chatReconnectDelay = Math.min(chatReconnectDelay * 2, 30000);
        }, chatReconnectDelay);
      };

      chatWs.onerror = function () {};
    }

    function disconnectChat() {
      if (chatReconnectTimer) { clearTimeout(chatReconnectTimer); chatReconnectTimer = null; }
      if (chatWs) { chatWs.close(); chatWs = null; }
    }

    function sendChat(text) {
      if (!chatWs || chatWs.readyState !== WebSocket.OPEN) return;
      chatWs.send(JSON.stringify({ type: 'chat', text: text }));
    }

    function renderChatHistory(messages) {
      var container = document.getElementById('chat-messages');
      if (!container) return;
      container.innerHTML = '';
      for (var i = 0; i < messages.length; i++) {
        appendChatMessageDOM(container, messages[i]);
      }
      container.scrollTop = container.scrollHeight;
    }

    function appendChatMessage(msg) {
      var container = document.getElementById('chat-messages');
      if (!container) return;
      appendChatMessageDOM(container, msg);
      container.scrollTop = container.scrollHeight;
    }

    function appendChatMessageDOM(container, msg) {
      var div = document.createElement('div');
      div.className = msg.system ? 'chat-msg chat-msg-system' : 'chat-msg';
      div.innerHTML =
        '<span class="chat-msg-name">' + escapeHTML(msg.senderName) + ':</span>' +
        '<span class="chat-msg-text">' + escapeHTML(msg.text) + '</span>';
      container.appendChild(div);
    }

    // --- Chat input binding ---
    var chatInput = document.getElementById('chat-input');
    var chatSendBtn = document.getElementById('chat-send');
    if (chatInput && chatSendBtn) {
      chatSendBtn.addEventListener('click', function () {
        var text = chatInput.value.trim();
        if (text) { sendChat(text); chatInput.value = ''; }
      });
      chatInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          var text = chatInput.value.trim();
          if (text) { sendChat(text); chatInput.value = ''; }
        }
      });
    }

    // Chat collapse toggle (Twitch-style: fully hidden when collapsed)
    var chatToggle = document.getElementById('chat-toggle');
    var chatPanel = document.getElementById('game-chat');
    var chatExpandBtn = document.getElementById('chat-expand');
    if (chatToggle && chatPanel && chatExpandBtn) {
      function setChatCollapsed(collapsed) {
        if (collapsed) {
          chatPanel.classList.add('collapsed');
          chatExpandBtn.classList.add('visible');
        } else {
          chatPanel.classList.remove('collapsed');
          chatExpandBtn.classList.remove('visible');
        }
      }
      // Collapse by default on mobile
      if (window.innerWidth <= 900) setChatCollapsed(true);
      chatToggle.addEventListener('click', function () { setChatCollapsed(true); });
      chatExpandBtn.addEventListener('click', function () { setChatCollapsed(false); });
    }

    // --- HUD rendering ---

    var hudPnlLimit = 100; // default: recent 100 hands

    function renderHudSparkline(hands, limit) {
      var el = document.getElementById('hud-sparkline');
      if (!el) return;
      if (!hands || hands.length === 0) {
        el.innerHTML = '<div style="color:var(--text-dim);font-size:var(--text-xs)">No data</div>';
        return;
      }

      var sorted = hands.slice().sort(function (a, b) { return a.timestamp - b.timestamp; });
      if (limit > 0 && sorted.length > limit) sorted = sorted.slice(sorted.length - limit);
      var cumulative = [0];
      var sum = 0;
      for (var i = 0; i < sorted.length; i++) {
        sum += sorted[i].delta;
        cumulative.push(sum);
      }

      var n = cumulative.length;
      var min = Math.min.apply(null, cumulative);
      var max = Math.max.apply(null, cumulative);
      var range = max - min || 1;

      var W = 200, H = 70, pad = 2;
      var points = [];
      for (var i = 0; i < n; i++) {
        var x = pad + (i / (n - 1)) * (W - 2 * pad);
        var y = pad + (1 - (cumulative[i] - min) / range) * (H - 2 * pad);
        points.push(x.toFixed(1) + ',' + y.toFixed(1));
      }

      var last = cumulative[n - 1];
      var color = last >= 0 ? 'var(--positive)' : 'var(--negative)';

      el.innerHTML =
        '<svg viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none">' +
        '<polyline fill="none" stroke="' + color + '" stroke-width="2" stroke-linejoin="round" points="' + points.join(' ') + '"/>' +
        '</svg>';
    }

    // P&L range filter buttons
    var hudPnlBtns = document.querySelectorAll('.hud-pnl-btn');
    for (var hf = 0; hf < hudPnlBtns.length; hf++) {
      (function (btn) {
        btn.addEventListener('click', function () {
          for (var j = 0; j < hudPnlBtns.length; j++) hudPnlBtns[j].classList.remove('hud-pnl-btn-active');
          btn.classList.add('hud-pnl-btn-active');
          hudPnlLimit = parseInt(btn.dataset.limit, 10);
          if (allChartHands.length > 0) renderHudSparkline(allChartHands, hudPnlLimit);
        });
      })(hudPnlBtns[hf]);
    }

    var PLAN_LETTERS = ['A', 'B', 'C', 'D'];
    var COMP_COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

    function renderHudPlans(data) {
      var el = document.getElementById('hud-plans-list');
      if (!el) return;
      var plans = (data && data.gamePlans) || [];
      var recs = (data && data.recommended) || [];

      if (plans.length === 0 && recs.length === 0) {
        el.innerHTML = '<div style="color:var(--text-dim);font-size:var(--text-xs)">No plans</div>';
        return;
      }

      var html = '';
      var count = Math.min(plans.length, 4);
      for (var i = 0; i < count; i++) {
        var p = plans[i];
        var letter = PLAN_LETTERS[i];
        var cls = p.active ? 'hud-plan hud-plan-active' : 'hud-plan';
        html += '<div class="' + cls + '">';
        html += '<div class="hud-plan-letter">' + letter + '</div>';
        html += '<div class="hud-plan-name">' + escapeHTML(p.name) + '</div>';
        var comps = p.distribution || [];
        for (var j = 0; j < comps.length; j++) {
          var label = comps[j].ref ? comps[j].ref.toUpperCase() : escapeHTML(comps[j].name || '');
          var pct = Math.round(comps[j].weight * 100);
          var color = COMP_COLORS[j % COMP_COLORS.length];
          html += '<div class="hud-comp">';
          html += '<span class="hud-comp-label">' + label + '</span>';
          html += '<span class="hud-comp-pct">' + pct + '%</span>';
          html += '</div>';
          html += '<div class="hud-comp-bar"><div class="hud-comp-fill" style="width:' + pct + '%;background:' + color + '"></div></div>';
        }
        html += '</div>';
      }
      // Show 1 recommended plan in the next slot
      if (recs.length > 0 && count < 4) {
        var rec = recs[0];
        var rl = PLAN_LETTERS[count];
        html += '<div class="hud-plan hud-plan-rec">';
        html += '<div class="hud-plan-letter">' + rl + '</div>';
        html += '<div class="hud-plan-name">' + escapeHTML(rec.name) + '</div>';
        var rc = rec.distribution || [];
        for (var k = 0; k < rc.length; k++) {
          var rlabel = rc[k].ref ? rc[k].ref.toUpperCase() : escapeHTML(rc[k].name || '');
          var rpct = Math.round(rc[k].weight * 100);
          var rcolor = COMP_COLORS[k % COMP_COLORS.length];
          html += '<div class="hud-comp">';
          html += '<span class="hud-comp-label">' + rlabel + '</span>';
          html += '<span class="hud-comp-pct">' + rpct + '%</span>';
          html += '</div>';
          html += '<div class="hud-comp-bar"><div class="hud-comp-fill" style="width:' + rpct + '%;background:' + rcolor + '"></div></div>';
        }
        html += '<div class="hud-rec-badge">RECOMMEND</div>';
        html += '</div>';
      }
      el.innerHTML = html;
    }

    function renderHudStats(balance, lbData, agentId, stats) {
      var el = document.getElementById('hud-stats-grid');
      if (!el) return;

      var balStr = balance ? formatChips(balance.balance) : '\u2014';
      var handsStr = '0';
      var winrateStr = '\u2014';
      var profitStr = '\u2014';
      var profitColor = '';
      var rankStr = '\u2014';
      var streakStr = '\u2014';
      var streakColor = '';

      var entry = null;
      var entries = (lbData && lbData.leaderboard) || [];
      for (var i = 0; i < entries.length; i++) {
        if (entries[i].agentId === agentId) { entry = entries[i]; break; }
      }

      if (entry) {
        handsStr = (entry.handsPlayed || 0).toLocaleString();
        var hands = entry.handsPlayed || 0;
        var wins = entry.wins || 0;
        winrateStr = hands > 0 ? Math.round((wins / hands) * 100) + '%' : '0%';
        var profit = entry.netProfit || 0;
        profitStr = (profit >= 0 ? '+' : '') + formatChips(profit);
        profitColor = profit >= 0 ? 'var(--positive)' : 'var(--negative)';
        var rank = entries.indexOf(entry) + 1;
        var pct = (rank / entries.length * 100);
        rankStr = 'Top ' + (pct < 1 ? pct.toFixed(1) : Math.round(pct)) + '%';
      } else if (balance) {
        handsStr = (balance.handsPlayed || 0).toLocaleString();
      }

      if (stats && stats.currentStreak) {
        var s = stats.currentStreak;
        if (s > 0) { streakStr = 'W' + s; streakColor = 'var(--positive)'; }
        else if (s < 0) { streakStr = 'L' + Math.abs(s); streakColor = 'var(--negative)'; }
      }

      el.innerHTML =
        hudStatCell(balStr, 'Balance') +
        hudStatCell(handsStr, 'Hands') +
        hudStatCell(winrateStr, 'Win Rate') +
        hudStatCell(profitStr, 'Net P/L', profitColor) +
        hudStatCell(streakStr, 'Streak', streakColor) +
        hudStatCell(rankStr, 'Ranking');
    }

    function hudStatCell(value, label, color) {
      var style = color ? ' style="color:' + color + '"' : '';
      return '<div class="hud-stat">' +
        '<div class="hud-stat-val"' + style + '>' + value + '</div>' +
        '<div class="hud-stat-label">' + label + '</div>' +
        '</div>';
    }

    function loadDashboard(agentId) {
      // Phase 1: Instant data — summary cards + profile + position + variance + leaderboard
      var leaderboardPromise = fetch('/api/leaderboard').then(function (r) { return r.json(); });
      Promise.all([
        authFetch('/api/escrow/balance').then(function (r) { return r.ok ? r.json() : null; }),
        leaderboardPromise,
        authFetch('/api/stats/' + encodeURIComponent(agentId)).then(function (r) { return r.ok ? r.json() : null; }),
      ]).then(function (results) {
        renderOverview(agentId, results[0], results[1], results[2]);
        renderHudStats(results[0], results[1], agentId, results[2]);
        if (results[2]) {
          renderProfile(results[2]);
          renderPositionStats(results[2]);
        }
      }).catch(function (err) {
        console.error('Summary load error:', err);
      });

      // Game tab (needs /api/tables) + reuse leaderboard from Phase 1
      Promise.all([
        leaderboardPromise,
        fetch('/api/tables?bigBlind_gte=0').then(function (r) { return r.json(); }),
      ]).then(function (results) {
        renderDashLeaderboard(results[0], results[1], agentId);

        // Find agent's current table (uses unsampled full table list)
        var tables = (results[1] && results[1].tables) || [];
        var agentTableId = null;
        for (var t = 0; t < tables.length; t++) {
          var pids = tables[t].players || tables[t].playerIds || [];
          if (pids.indexOf(agentId) !== -1) {
            agentTableId = tables[t].tableId;
            break;
          }
        }

        // Set default tab on first load
        if (!defaultTabSet) {
          defaultTabSet = true;
          activateTab(agentTableId ? 'game' : 'overview');
        }

        // Render Game tab live stream
        renderGameLive(agentTableId);

        // Connect/disconnect chat
        if (agentTableId && dashAgentIdForEmbed) {
          connectChat(agentTableId, dashAgentIdForEmbed);
        } else {
          disconnectChat();
        }
      }).catch(function (err) {
        console.error('Leaderboard load error:', err);
        var el = document.getElementById('dash-leaderboard');
        if (el) el.innerHTML = '<div class="dash-empty">Failed to load leaderboard.</div>';
        if (!defaultTabSet) { defaultTabSet = true; activateTab('overview'); }
      });

      // Game plan + per-plan stats (authenticated, private)
      Promise.all([
        authFetch('/api/game-plan').then(function (r) { return r.ok ? r.json() : null; }),
        authFetch('/api/game-plan/stats').then(function (r) { return r.ok ? r.json() : null; }),
      ]).then(function (results) {
        var gpData = results[0];
        var statsData = results[1];
        renderHudPlans(gpData);
        renderGamePlan(gpData, document.getElementById('overview-gameplan-content'), statsData);
        populateGpFilter(gpData);
      }).catch(function (err) { console.error('Game plan load error:', err); });

      // Phase 2a: First page of hand history
      fetchHandPage(agentId, null).then(function (result) {
        renderHandHistory(agentId, result.hands, result.hasMore, result.cursor);
      }).catch(function (err) {
        console.error('History load error:', err);
        historyEl.innerHTML = '<div class="dash-empty">Failed to load hand history.</div>';
      });

      // Phase 2b: Logs for P&L chart + sparkline (refreshes every cycle)
      if (!chartFetchInFlight) {
        chartFetchInFlight = true;
        authFetch('/api/logs?limit=1000').then(function (r) { return r.json(); }).then(function (body) {
          var logs = body.logs || [];
          var hands = [];
          for (var i = 0; i < logs.length; i++) {
            var players = logs[i].players || [];
            for (var j = 0; j < players.length; j++) {
              if (players[j].agentId === agentId) {
                hands.push({ handId: logs[i].handId, tableId: logs[i].tableId, timestamp: logs[i].timestamp, delta: players[j].delta || 0 });
                break;
              }
            }
          }
          allChartHands = hands;
          allHandsFetched = false;
          renderChart(hands, chartLimit);
          renderHudSparkline(hands, hudPnlLimit);
        }).catch(function (err) {
          console.error('Chart load error:', err);
        }).finally(function () {
          chartFetchInFlight = false;
        });
      }
    }

    // --- Data fetching ---

    function fetchAgentLogs(agentId) {
      var allHands = [];
      var MAX_PAGES = 5;
      var pageCount = 0;
      function fetchPage(cursor) {
        var url = '/api/logs?limit=1000&agentId=' + encodeURIComponent(agentId);
        if (cursor) url += '&cursor=' + encodeURIComponent(cursor);
        return authFetch(url)
          .then(function (r) { return r.json(); })
          .then(function (body) {
            var logs = body.logs || [];
            for (var i = 0; i < logs.length; i++) {
              var log = logs[i];
              var players = log.players || [];
              // Compute totalPot: use stored value, or approximate from sum of |deltas|
              var pot = log.totalPot || 0;
              if (!pot && players.length > 0) {
                for (var k = 0; k < players.length; k++) {
                  pot += Math.abs(players[k].delta || 0);
                }
              }
              for (var j = 0; j < players.length; j++) {
                if (players[j].agentId === agentId) {
                  allHands.push({
                    handId: log.handId,
                    tableId: log.tableId,
                    timestamp: log.timestamp,
                    delta: players[j].delta || 0,
                    maxCommitment: players[j].maxCommitment || 0,
                    streetsReached: players[j].streetsReached || 0,
                    playerName: players[j].name,
                  });
                  break;
                }
              }
            }
            pageCount++;
            if (body.hasMore && body.cursor && pageCount < MAX_PAGES) {
              return fetchPage(body.cursor);
            }
            return allHands;
          });
      }
      return fetchPage(null);
    }

    function fetchHandPage(agentId, cursor) {
      var url = '/api/logs?limit=20&agentId=' + encodeURIComponent(agentId);
      if (cursor) url += '&cursor=' + encodeURIComponent(cursor);
      return authFetch(url)
        .then(function (r) { return r.json(); })
        .then(function (body) {
          var hands = [];
          var logs = body.logs || [];
          for (var i = 0; i < logs.length; i++) {
            var log = logs[i];
            var players = log.players || [];
            for (var j = 0; j < players.length; j++) {
              if (players[j].agentId === agentId) {
                hands.push({
                  handId: log.handId,
                  tableId: log.tableId,
                  timestamp: log.timestamp,
                  delta: players[j].delta || 0,
                  playerName: players[j].name,
                });
                break;
              }
            }
          }
          return { hands: hands, cursor: body.cursor || null, hasMore: !!body.hasMore };
        });
    }

    var handDetailCache = {};

    function fetchHandDetail(tableId, handId) {
      if (handDetailCache[handId]) return Promise.resolve(handDetailCache[handId]);
      return authFetch('/api/tables/' + encodeURIComponent(tableId) + '/hands/' + encodeURIComponent(handId))
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (data) {
          if (data) handDetailCache[handId] = data;
          return data;
        });
    }

    // Derive streetsReached from full hand records for hands missing it
    var phaseToStreet = { preflop: 1, flop: 2, turn: 3, river: 4, showdown: 4 };

    function deriveStreetsFromRecord(record, agentId) {
      if (!record || !record.actions) return 0;
      var max = 0;
      for (var i = 0; i < record.actions.length; i++) {
        var a = record.actions[i];
        if (a.agentId === agentId) {
          var s = phaseToStreet[a.phase] || 0;
          if (s > max) max = s;
        }
      }
      return max || 1; // at minimum preflop if record exists
    }

    function enrichStreetsReached(hands, agentId) {
      var missing = [];
      for (var i = 0; i < hands.length; i++) {
        if (!hands[i].streetsReached) missing.push(hands[i]);
      }
      if (missing.length === 0) return Promise.resolve(hands);

      // Batch fetch hand details (max 50 concurrent to avoid overwhelming)
      var batch = missing.slice(0, 50);
      var promises = batch.map(function (h) {
        return fetchHandDetail(h.tableId, h.handId).then(function (record) {
          if (record) h.streetsReached = deriveStreetsFromRecord(record, agentId);
        }).catch(function () {});
      });
      return Promise.all(promises).then(function () { return hands; });
    }

    // --- Card formatting ---

    var SUIT_SYMBOLS = { hearts: '\u2665', diamonds: '\u2666', clubs: '\u2663', spades: '\u2660' };
    var RED_SUITS = { hearts: true, diamonds: true };

    function formatCard(card) {
      if (!card) return '?';
      var sym = SUIT_SYMBOLS[card.suit] || '?';
      var cls = RED_SUITS[card.suit] ? 'card-red' : 'card-white';
      return '<span class="card-glyph ' + cls + '">' + escapeHTML(card.rank) + sym + '</span>';
    }

    function formatCards(cards) {
      if (!cards || cards.length === 0) return '<span class="text-dim">none</span>';
      return cards.map(formatCard).join(' ');
    }

    // --- Hand detail rendering ---

    function renderHandDetail(record, agentId) {
      if (!record) return '<div class="hand-detail-inner text-dim">Detailed record not available for this hand.</div>';

      var html = '<div class="hand-detail-inner">';

      var cc = record.communityCards || [];
      if (cc.length > 0) {
        html += '<div class="hd-row"><span class="hd-label">Board</span>';
        html += '<span class="hd-cards">';
        if (cc.length >= 3) html += formatCards(cc.slice(0, 3));
        if (cc.length >= 4) html += ' <span class="hd-street">|</span> ' + formatCard(cc[3]);
        if (cc.length >= 5) html += ' <span class="hd-street">|</span> ' + formatCard(cc[4]);
        html += '</span></div>';
      }

      var holeCards = record.playerHoleCards && record.playerHoleCards[agentId];
      if (holeCards) {
        html += '<div class="hd-row"><span class="hd-label">Your Hand</span><span class="hd-cards">' + formatCards(holeCards) + '</span></div>';
      }

      var winners = record.winners || [];
      if (winners.length > 0) {
        html += '<div class="hd-row"><span class="hd-label">Winner</span><span>';
        for (var w = 0; w < winners.length; w++) {
          var win = winners[w];
          var name = win.agentId === agentId ? 'You' : (win.agentId.length > 12 ? win.agentId.slice(0, 8) + '\u2026' : win.agentId);
          html += escapeHTML(name) + ' won ' + formatChips(win.amount);
          if (win.hand) {
            var rankNames = ['High Card','Pair','Two Pair','Three of a Kind','Straight','Flush','Full House','Four of a Kind','Straight Flush','Royal Flush'];
            html += ' <span class="text-dim">(' + (rankNames[win.hand.rank] || '?') + ')</span>';
          }
          if (w < winners.length - 1) html += ', ';
        }
        html += '</span></div>';
      }

      var pots = record.pots || [];
      var totalPot = 0;
      for (var p = 0; p < pots.length; p++) totalPot += pots[p].amount;
      if (totalPot > 0) {
        html += '<div class="hd-row"><span class="hd-label">Pot</span><span>' + formatChips(totalPot);
        if (record.rake) html += ' <span class="text-dim">(rake ' + formatChips(record.rake) + ')</span>';
        html += '</span></div>';
      }

      var actions = record.actions || [];
      if (actions.length > 0) {
        html += '<div class="hd-actions"><div class="hd-label">Actions</div>';
        var curPhase = '';
        for (var a = 0; a < actions.length; a++) {
          var act = actions[a];
          if (act.phase !== curPhase) {
            curPhase = act.phase;
            html += '<div class="hd-phase">' + escapeHTML(curPhase) + '</div>';
          }
          var actName = act.agentId === agentId ? 'You' : (act.agentId.length > 12 ? act.agentId.slice(0, 8) + '\u2026' : act.agentId);
          var actStr = act.action;
          if (act.amount > 0 && act.action !== 'fold' && act.action !== 'check') {
            actStr += ' ' + formatChips(act.amount);
          }
          html += '<div class="hd-action"><span class="hd-actor">' + escapeHTML(actName) + '</span> <span>' + escapeHTML(actStr) + '</span></div>';
        }
        html += '</div>';
      }

      html += '</div>';
      return html;
    }

    // --- Stats derivation ---

    function deriveStats(s) {
      if (!s || !s.hands) return null;
      var pct = function (n, d) { return d > 0 ? Math.round(n / d * 1000) / 10 : 0; };
      var vpip = pct(s.vpipHands, s.hands);
      var pfr = pct(s.pfrHands, s.hands);
      var af = s.passiveActions > 0 ? Math.round(s.aggressiveActions / s.passiveActions * 100) / 100 : 0;
      var type = 'Unknown';
      if (s.hands >= 20) {
        var tight = vpip < 25;
        var agg = af > 1.5 || pfr > 15;
        if (tight && agg) type = 'TAG';
        else if (!tight && agg) type = 'LAG';
        else if (tight && !agg) type = 'Rock';
        else type = 'Calling Station';
      }
      var mean = s.totalProfit / s.hands;
      var variance = (s.sumSquaredDeltas / s.hands) - (mean * mean);
      return {
        vpipPct: vpip, pfrPct: pfr,
        threeBetPct: pct(s.threeBetHands, s.hands),
        af: af,
        wtsdPct: pct(s.showdownHands, s.hands),
        wsdPct: pct(s.showdownWins, s.showdownHands),
        cbetPct: pct(s.cbetMade, s.cbetOpportunities),
        foldPct: pct(s.folds, s.hands),
        stdDev: Math.round(Math.sqrt(Math.max(0, variance))),
        playerType: type,
      };
    }

    // --- Tab 1: Overview (merged summary + variance into 5x2 grid) ---

    function renderOverview(agentId, balance, lbData, stats) {
      var balEl = document.getElementById('dc-balance');
      var handsEl = document.getElementById('dc-hands');
      var winrateEl = document.getElementById('dc-winrate');
      var profitEl = document.getElementById('dc-profit');
      var rankingEl = document.getElementById('dc-ranking');

      // Escrow banner
      var bannerEl = document.getElementById('escrow-banner');
      if (balance && bannerEl) {
        var usd = (balance.balanceUsdcAtomic / 1000000).toFixed(2);
        var wStatus = balance.withdrawalUnlocked
          ? '<span style="color:var(--positive)">withdraw unlocked</span>'
          : '<span>withdraw locked (' + balance.handsUntilWithdrawal + ' more hands)</span>';
        var vaultLink = balance.vaultAddress
          ? '<a href="https://explorer.solana.com/address/' + balance.vaultAddress + '?cluster=devnet" target="_blank" class="escrow-link" title="Verify on-chain">'
          : '<span>';
        var vaultClose = balance.vaultAddress ? '</a>' : '</span>';
        bannerEl.innerHTML =
          vaultLink + 'Escrow: <span class="escrow-value">' + balance.balance + ' chips ($' + usd + ' USDC)</span> &#x1F517;' + vaultClose +
          '<span class="escrow-withdraw">' + wStatus + '</span>';
      }

      if (balance) {
        balEl.textContent = formatChips(balance.balance);
      }

      var entry = null;
      var entries = (lbData && lbData.leaderboard) || [];
      for (var i = 0; i < entries.length; i++) {
        if (entries[i].agentId === agentId) { entry = entries[i]; break; }
      }

      if (entry) {
        handsEl.textContent = (entry.handsPlayed || 0).toLocaleString();
        var hands = entry.handsPlayed || 0;
        var wins = entry.wins || 0;
        winrateEl.textContent = hands > 0 ? Math.round((wins / hands) * 100) + '%' : '0%';
        var profit = entry.netProfit || 0;
        profitEl.textContent = (profit >= 0 ? '+' : '') + formatChips(profit);
        profitEl.style.color = profit >= 0 ? 'var(--positive)' : 'var(--negative)';
      } else {
        handsEl.textContent = balance ? (balance.handsPlayed || 0).toLocaleString() : '0';
        winrateEl.textContent = '\u2014';
        profitEl.textContent = '\u2014';
      }

      // Ranking percentile from leaderboard position
      if (entry && entries.length > 0) {
        var rank = entries.indexOf(entry) + 1;
        var pct = (rank / entries.length * 100);
        rankingEl.textContent = 'Top ' + (pct < 1 ? pct.toFixed(2) : Math.round(pct)) + '%';
      }

      // Variance from stats
      var d = deriveStats(stats);
      if (d) {
        document.getElementById('dc-stddev').textContent = formatChips(d.stdDev);
      }
      if (stats && stats.hands) {
        document.getElementById('dc-drawdown').textContent = formatChips(stats.maxDrawdown);
        document.getElementById('dc-bigwin').textContent = '+' + formatChips(stats.biggestWin);
        document.getElementById('dc-bigloss').textContent = formatChips(stats.biggestLoss);
        var streak = stats.currentStreak || 0;
        var streakEl = document.getElementById('dc-streak');
        if (streak > 0) {
          streakEl.textContent = 'Win ' + streak;
          streakEl.style.color = 'var(--positive)';
        } else if (streak < 0) {
          streakEl.textContent = 'Lose ' + Math.abs(streak);
          streakEl.style.color = 'var(--negative)';
        } else {
          streakEl.textContent = '\u2014';
        }
      }
    }

    // --- Tab 2: Behavioral Profile ---

    function renderProfile(stats) {
      var d = deriveStats(stats);
      if (!d) return;
      document.getElementById('st-vpip').textContent = d.vpipPct.toFixed(1) + '%';
      document.getElementById('st-pfr').textContent = d.pfrPct.toFixed(1) + '%';
      document.getElementById('st-3bet').textContent = d.threeBetPct.toFixed(1) + '%';
      document.getElementById('st-af').textContent = d.af.toFixed(2);
      document.getElementById('st-wtsd').textContent = d.wtsdPct.toFixed(1) + '%';
      document.getElementById('st-wsd').textContent = d.wsdPct.toFixed(1) + '%';
      document.getElementById('st-cbet').textContent = d.cbetPct.toFixed(1) + '%';
      document.getElementById('st-fold').textContent = d.foldPct.toFixed(1) + '%';

      var ctx = document.getElementById('radar-chart').getContext('2d');
      if (charts.radar) charts.radar.destroy();
      charts.radar = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: ['VPIP', 'PFR', 'AF', 'WTSD', 'C-Bet'],
          datasets: [{
            data: [
              Math.min(d.vpipPct, 100),
              Math.min(d.pfrPct, 100),
              Math.min(d.af * 20, 100),
              Math.min(d.wtsdPct, 100),
              Math.min(d.cbetPct, 100),
            ],
            borderColor: '#4AE176',
            backgroundColor: 'rgba(74, 225, 118, 0.12)',
            borderWidth: 2,
            pointBackgroundColor: '#4AE176',
            pointRadius: 3,
          }],
        },
        options: {
          responsive: true,
          animation: false,
          maintainAspectRatio: true,
          plugins: { legend: { display: false } },
          scales: {
            r: {
              beginAtZero: true,
              max: 100,
              ticks: { display: false, stepSize: 25 },
              grid: { color: 'rgba(255,255,255,0.06)' },
              angleLines: { color: 'rgba(255,255,255,0.06)' },
              pointLabels: { color: '#71717a', font: { size: 11 } },
            },
          },
        },
      });
    }

    // --- Tab 3: Position Stats ---

    function renderPositionStats(stats) {
      if (!stats || !stats.positions) return;
      var positions = ['EP', 'MP', 'CO', 'BTN', 'SB', 'BB'];
      var hasData = false;
      for (var i = 0; i < positions.length; i++) {
        if (stats.positions[positions[i]] && stats.positions[positions[i]].hands > 0) {
          hasData = true; break;
        }
      }
      if (!hasData) return;

      var profits = [];
      var colors = [];
      var tbody = document.getElementById('pos-table-body');
      var html = '';
      for (var i = 0; i < positions.length; i++) {
        var p = stats.positions[positions[i]] || { hands: 0, vpip: 0, pfr: 0, profit: 0 };
        profits.push(p.profit);
        colors.push(p.profit >= 0 ? '#4AE176' : '#f87171');
        var vpipPct = p.hands > 0 ? (p.vpip / p.hands * 100).toFixed(1) : '0.0';
        var pfrPct = p.hands > 0 ? (p.pfr / p.hands * 100).toFixed(1) : '0.0';
        var profitStr = (p.profit >= 0 ? '+' : '') + formatChips(p.profit);
        var profitColor = p.profit >= 0 ? 'var(--positive)' : 'var(--negative)';
        html += '<tr><td>' + positions[i] + '</td><td>' + p.hands + '</td><td>' + vpipPct + '%</td><td>' + pfrPct + '%</td><td style="color:' + profitColor + '">' + profitStr + '</td></tr>';
      }
      tbody.innerHTML = html;

      var ctx = document.getElementById('position-chart').getContext('2d');
      if (charts.position) charts.position.destroy();
      charts.position = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: positions,
          datasets: [{
            data: profits.map(function (v) { return v / 100; }),
            backgroundColor: colors.map(function (c) { return c + '33'; }),
            borderColor: colors,
            borderWidth: 1,
            borderRadius: 4,
          }],
        },
        options: {
          responsive: true,
          animation: false,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: {
              ticks: { color: '#71717a', font: { size: 11 } },
              grid: { display: false },
            },
            y: {
              ticks: {
                color: '#71717a',
                font: { size: 11 },
                callback: function (v) { return '$' + v.toFixed(2); },
              },
              grid: { color: 'rgba(255,255,255,0.04)' },
            },
          },
        },
      });
    }

    // --- Tab 4: Leaderboard ---

    function renderDashLeaderboard(lbData, tablesData, myAgentId) {
      var el = document.getElementById('dash-leaderboard');
      if (!el) return;
      var entries = (lbData && lbData.leaderboard) || [];
      var tables = (tablesData && tablesData.tables) || [];

      // Build online map: agentId → tableId
      var online = {};
      for (var t = 0; t < tables.length; t++) {
        var ids = tables[t].playerIds || [];
        for (var p = 0; p < ids.length; p++) {
          online[ids[p]] = tables[t].tableId;
        }
      }

      if (entries.length === 0) {
        el.innerHTML = '<div class="dash-empty">No agents on the leaderboard yet.</div>';
        return;
      }

      var html =
        '<table class="lb-table"><thead><tr>' +
        '<th>#</th><th>Agent</th><th>Hands</th><th>Win Rate</th><th>Net Profit</th>' +
        '</tr></thead><tbody>';

      for (var i = 0; i < entries.length; i++) {
        var e = entries[i];
        var profit = e.netProfit || 0;
        var profitClass = profit >= 0 ? 'lb-positive' : 'lb-negative';
        var profitStr = profit >= 0 ? '+' + formatChips(profit) : formatChips(profit);
        var hands = e.handsPlayed || 0;
        var wins = e.wins || 0;
        var winRate = hands > 0 ? Math.round((wins / hands) * 100) + '%' : '\u2014';

        var tableId = online[e.agentId];
        var isMe = e.agentId === myAgentId;
        var nameHtml;
        if (tableId && isMe) {
          // Current agent: dot on left
          nameHtml = '<span class="online-dot online-dot-left"></span><a href="/table.html?id=' + encodeURIComponent(tableId) + '" class="lb-link">' + escapeHTML(e.name || e.agentId) + '</a>';
        } else if (tableId) {
          // Other online agents: dot on right
          nameHtml = '<a href="/table.html?id=' + encodeURIComponent(tableId) + '" class="lb-link">' + escapeHTML(e.name || e.agentId) + '</a><span class="online-dot online-dot-right"></span>';
        } else {
          nameHtml = escapeHTML(e.name || e.agentId);
        }

        html +=
          '<tr>' +
            '<td class="lb-rank">' + (i + 1) + '</td>' +
            '<td class="lb-name">' + nameHtml + '</td>' +
            '<td class="lb-hands">' + hands + '</td>' +
            '<td class="lb-winrate">' + winRate + '</td>' +
            '<td class="lb-profit ' + profitClass + '">' + escapeHTML(profitStr) + '</td>' +
          '</tr>';
      }

      html += '</tbody></table>';
      el.innerHTML = html;
    }

    // --- Game Live Stream ---

    var dashAgentIdForEmbed = '';
    function renderGameLive(tableId) {
      var el = document.getElementById('game-live');
      if (!el) return;

      var tableIdEl = document.getElementById('chat-table-id');

      if (!tableId) {
        if (currentEmbedTableId || (!el.querySelector('iframe') && !el.querySelector('.game-live-empty'))) {
          currentEmbedTableId = null;
          el.innerHTML =
            '<div class="dash-empty game-live-empty">' +
            'Not at a table.<br>Join a table via the API to see your game live.' +
            '</div>';
          if (tableIdEl) tableIdEl.innerHTML = '';
        }
        return;
      }

      // Only update iframe if table + agent unchanged
      var embedKey = tableId + ':' + dashAgentIdForEmbed;
      if (currentEmbedTableId === embedKey) return;
      currentEmbedTableId = embedKey;

      el.innerHTML =
        '<iframe class="game-iframe" ' +
        'src="/table.html?id=' + encodeURIComponent(tableId) + '&embed=1&agentId=' + encodeURIComponent(dashAgentIdForEmbed) + '" ' +
        'title="Live Table"></iframe>';

      if (tableIdEl) {
        tableIdEl.innerHTML = '<span class="chat-table-id-btn" title="Click to copy table ID">' + escapeHTML(tableId) + '</span>';
        tableIdEl.querySelector('.chat-table-id-btn').addEventListener('click', function () {
          navigator.clipboard.writeText(tableId).then(function () {
            var btn = tableIdEl.querySelector('.chat-table-id-btn');
            var orig = btn.textContent;
            btn.textContent = 'Copied!';
            setTimeout(function () { btn.textContent = orig; }, 1500);
          });
        });
      }
    }

    // --- Game Plan ---

    function renderGamePlan(data, targetEl, statsData) {
      if (!targetEl) return;

      var plans = (data && data.gamePlans) || [];
      if (plans.length === 0) {
        targetEl.innerHTML =
          '<div class="dash-empty">' +
          'No game plan declared.<br>' +
          'See <a href="/skill.md">sharkclaw.ai/skill.md</a> to set up your first game plan.' +
          '</div>';
        return;
      }

      // Build stats lookup: planId → stats
      var statsMap = {};
      if (statsData && statsData.plans) {
        for (var s = 0; s < statsData.plans.length; s++) {
          statsMap[statsData.plans[s].planId] = statsData.plans[s];
        }
      }

      // Sort: active plan first
      var sorted = plans.slice().sort(function (a, b) {
        return (b.active === true ? 1 : 0) - (a.active === true ? 1 : 0);
      });

      var html = '';
      for (var i = 0; i < sorted.length; i++) {
        var plan = sorted[i];
        var isActive = plan.active === true;
        var cardClass = isActive ? 'gp-card gp-active' : 'gp-card gp-inactive';
        var ps = statsMap[plan.id];
        var uid = targetEl.id + '-' + plan.id;

        html += '<div class="' + cardClass + '">';
        html += '<div class="gp-header">';
        html += '<div class="gp-header-left">';
        html += '<h3 class="gp-name">' + escapeHTML(plan.name);
        if (isActive) html += ' <span class="gp-badge">Active</span>';
        html += '</h3>';
        if (plan.description) {
          html += '<p class="gp-desc">' + escapeHTML(plan.description) + '</p>';
        }
        html += '</div>';
        html += '<button class="gp-toggle" data-uid="' + uid + '" title="Toggle stats">Stats</button>';
        html += '</div>';

        html += '<div class="gp-views">';

        // Normal view (default)
        html += '<div class="gp-view gp-view-normal" id="' + uid + '-normal">';
        html += buildComponentList(plan.distribution);
        html += '</div>';

        // Stats view (hidden)
        html += '<div class="gp-view gp-view-stats" id="' + uid + '-stats" data-hidden>';
        if (ps && ps.hands > 0) {
          var winRate = Math.round((ps.wins / ps.hands) * 100);
          var lossRate = Math.round((ps.losses / ps.hands) * 100);
          var profitStr = (ps.totalProfit >= 0 ? '+' : '') + formatChips(ps.totalProfit);
          var profitClass = ps.totalProfit >= 0 ? 'gp-stat-pos' : 'gp-stat-neg';
          html += '<div class="gp-stats-grid">';
          html += '<div class="gp-stats-item"><div class="gp-stats-val">' + ps.hands + '</div><div class="gp-stats-label">Hands</div></div>';
          html += '<div class="gp-stats-item"><div class="gp-stats-val">' + winRate + '%</div><div class="gp-stats-label">Win Rate</div></div>';
          html += '<div class="gp-stats-item"><div class="gp-stats-val ' + profitClass + '">' + profitStr + '</div><div class="gp-stats-label">Net Profit</div></div>';
          html += '<div class="gp-stats-item"><div class="gp-stats-val gp-stat-pos">+' + formatChips(ps.biggestWin || 0) + '</div><div class="gp-stats-label">Best Hand</div></div>';
          html += '<div class="gp-stats-item"><div class="gp-stats-val gp-stat-neg">' + formatChips(ps.biggestLoss || 0) + '</div><div class="gp-stats-label">Worst Hand</div></div>';
          html += '<div class="gp-stats-item"><div class="gp-stats-val">' + lossRate + '%</div><div class="gp-stats-label">Loss Rate</div></div>';
          html += '</div>';
        } else {
          html += '<div class="dash-empty" style="padding:1rem 0;font-size:0.85rem">No hands played with this plan yet.</div>';
        }
        html += '</div>';

        html += '</div>'; // close .gp-views
        html += '</div>'; // close .gp-card
      }

      targetEl.innerHTML = html;

      // Bind toggle buttons
      var toggles = targetEl.querySelectorAll('.gp-toggle');
      for (var t = 0; t < toggles.length; t++) {
        (function (btn) {
          btn.addEventListener('click', function () {
            var uid = btn.dataset.uid;
            var normalEl = document.getElementById(uid + '-normal');
            var statsEl = document.getElementById(uid + '-stats');
            if (!normalEl || !statsEl) return;
            var showingStats = !statsEl.hasAttribute('data-hidden');
            if (showingStats) {
              normalEl.removeAttribute('data-hidden');
              statsEl.setAttribute('data-hidden', '');
            } else {
              normalEl.setAttribute('data-hidden', '');
              statsEl.removeAttribute('data-hidden');
            }
            btn.textContent = showingStats ? 'Stats' : 'Mix';
          });
        })(toggles[t]);
      }
    }

    function populateGpFilter(data) {
      var container = document.getElementById('gp-filter');
      if (!container) return;
      var plans = (data && data.gamePlans) || [];
      container.innerHTML = '<button class="pnl-filter active" data-plan="">All</button>';
      for (var i = 0; i < plans.length; i++) {
        var btn = document.createElement('button');
        btn.className = 'pnl-filter';
        btn.dataset.plan = plans[i].id;
        btn.textContent = plans[i].name;
        container.appendChild(btn);
      }
      // Bind click handlers
      var btns = container.querySelectorAll('.pnl-filter');
      for (var b = 0; b < btns.length; b++) {
        (function (btn) {
          btn.addEventListener('click', function () {
            for (var j = 0; j < btns.length; j++) btns[j].classList.remove('active');
            btn.classList.add('active');
            // TODO: filter analytics by btn.dataset.plan
          });
        })(btns[b]);
      }
    }

    function buildComponentList(distribution) {
      var colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16'];
      var html = '';
      for (var i = 0; i < distribution.length; i++) {
        var c = distribution[i];
        var pct = Math.round(c.weight * 100);
        var label = c.ref ? c.ref.toUpperCase() : escapeHTML(c.name || 'Custom');
        var desc = c.description ? escapeHTML(c.description) : (c.ref ? 'Catalog: ' + c.ref : '');
        var color = colors[i % colors.length];

        html += '<div class="gp-comp">';
        html += '<div class="gp-comp-header">';
        html += '<span class="gp-comp-dot" style="background:' + color + '"></span>';
        html += '<span class="gp-comp-label">' + label + '</span>';
        html += '<span class="gp-comp-pct">' + pct + '%</span>';
        html += '</div>';
        html += '<div class="gp-comp-bar"><div class="gp-comp-fill" style="width:' + pct + '%;background:' + color + '"></div></div>';
        if (desc) html += '<div class="gp-comp-desc">' + desc + '</div>';
        html += '</div>';
      }
      return html;
    }

    // --- P&L Chart (colored-segment line) ---

    function renderChart(agentHands, limit) {
      if (agentHands.length === 0) {
        chartEmpty.style.display = '';
        document.getElementById('tab-overview').querySelector('.chart-container').style.display = 'none';
        return;
      }

      var sorted = agentHands.slice().sort(function (a, b) { return a.timestamp - b.timestamp; });

      // Show last N hands (0 = all)
      var preDisplayCumulative = 0;
      if (limit > 0 && sorted.length > limit) {
        for (var s = 0; s < sorted.length - limit; s++) {
          preDisplayCumulative += sorted[s].delta;
        }
        sorted = sorted.slice(-limit);
      }

      // Build cumulative P&L line data + per-hand deltas for segment coloring
      var labels = [];
      var lineData = [];
      var deltas = [];
      var cumulative = preDisplayCumulative;
      for (var i = 0; i < sorted.length; i++) {
        var h = sorted[i];
        cumulative += h.delta;
        labels.push(new Date(h.timestamp).toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }));
        lineData.push(cumulative / 1000);
        deltas.push(h.delta);
      }

      var currentPnl = cumulative / 1000;
      var pnlColor = currentPnl >= 0 ? '#4AE176' : '#f87171';

      // Custom plugin: draw current P&L horizontal line + label
      var currentPnlPlugin = {
        id: 'currentPnlLine',
        afterDatasetsDraw: function (chart) {
          var yScale = chart.scales.y;
          var yPixel = yScale.getPixelForValue(currentPnl);
          var ctx = chart.ctx;
          var chartArea = chart.chartArea;
          ctx.save();
          ctx.strokeStyle = pnlColor;
          ctx.lineWidth = 0.5;
          ctx.setLineDash([4, 3]);
          ctx.beginPath();
          ctx.moveTo(chartArea.left, yPixel);
          ctx.lineTo(chartArea.right, yPixel);
          ctx.stroke();
          ctx.setLineDash([]);
          var label = '$' + currentPnl.toFixed(2);
          ctx.fillStyle = pnlColor;
          ctx.font = '11px sans-serif';
          ctx.textAlign = 'left';
          ctx.textBaseline = 'middle';
          ctx.fillRect(chartArea.right + 2, yPixel - 8, ctx.measureText(label).width + 6, 16);
          ctx.fillStyle = '#18181b';
          ctx.fillText(label, chartArea.right + 5, yPixel);
          ctx.restore();
        },
      };

      var ctx = document.getElementById('pnl-chart').getContext('2d');
      if (charts.pnl) charts.pnl.destroy();
      charts.pnl = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'P&L',
            data: lineData,
            borderWidth: 2,
            pointRadius: 0,
            pointHitRadius: 6,
            tension: 0,
            fill: false,
            // Color each segment green (win) or red (loss) based on the destination point's delta
            segment: {
              borderColor: function (c) {
                return deltas[c.p1DataIndex] >= 0 ? '#4AE176' : '#f87171';
              },
            },
          }],
        },
        plugins: [currentPnlPlugin],
        options: {
          responsive: true,
          animation: false,
          maintainAspectRatio: false,
          layout: { padding: { right: 60 } },
          interaction: { intersect: false, mode: 'index' },
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                title: function (items) { return items[0].label; },
                label: function (c) {
                  var d = deltas[c.dataIndex];
                  var sign = d >= 0 ? '+' : '';
                  return 'P&L: $' + c.parsed.y.toFixed(2) + ' (' + sign + (d / 1000).toFixed(2) + ')';
                },
              },
            },
          },
          scales: {
            x: {
              display: true,
              ticks: { color: '#71717a', maxTicksLimit: 8, font: { size: 11 } },
              grid: { color: 'rgba(255,255,255,0.04)' },
            },
            y: {
              display: true,
              position: 'left',
              ticks: {
                color: '#71717a',
                font: { size: 11 },
                callback: function (v) { return '$' + v.toFixed(2); },
              },
              grid: { color: 'rgba(255,255,255,0.04)' },
            },
          },
        },
      });
    }

    // --- Hand History (paginated) ---

    var dashAgentId = '';
    var currentPage = 0;
    var pageCursors = [null]; // cursor for each page (page 0 = null)
    var pageHasMore = false;

    function buildHandRow(h) {
      var time = new Date(h.timestamp).toLocaleString(undefined, {
        month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit',
      });
      var shortTable = h.tableId.length > 12
        ? h.tableId.slice(0, 6) + '\u2026' + h.tableId.slice(-4)
        : h.tableId;
      var resultClass = h.delta > 0 ? 'win' : h.delta < 0 ? 'loss' : 'push';
      var resultLabel = h.delta > 0 ? 'Win' : h.delta < 0 ? 'Loss' : 'Push';
      var deltaStr = (h.delta >= 0 ? '+' : '') + formatChips(h.delta);
      var deltaClass = h.delta > 0 ? 'delta-positive' : h.delta < 0 ? 'delta-negative' : 'delta-zero';

      return '<tr class="hand-row" data-hand-id="' + escapeHTML(h.handId) + '" data-table-id="' + escapeHTML(h.tableId) + '">' +
        '<td class="ht-toggle">\u25B8</td>' +
        '<td class="ht-time">' + escapeHTML(time) + '</td>' +
        '<td class="ht-table">' + escapeHTML(shortTable) + '</td>' +
        '<td><span class="result-badge ' + resultClass + '">' + resultLabel + '</span></td>' +
        '<td class="' + deltaClass + '">' + escapeHTML(deltaStr) + '</td>' +
      '</tr>' +
      '<tr class="hand-detail-row" id="detail-' + escapeHTML(h.handId) + '" style="display:none">' +
        '<td colspan="5"><div class="hand-detail-inner text-dim">Loading...</div></td>' +
      '</tr>';
    }

    function renderHandHistory(agentId, hands, hasMore, cursor) {
      dashAgentId = agentId;
      pageHasMore = hasMore;
      if (hasMore && cursor) {
        if (pageCursors.length <= currentPage + 1) pageCursors.push(cursor);
        else pageCursors[currentPage + 1] = cursor;
      }

      if (hands.length === 0 && currentPage === 0) {
        historyEl.innerHTML = '<div class="dash-empty">No hands played yet.</div>';
        return;
      }

      var html = '<table class="hand-table"><thead><tr>' +
        '<th></th><th>Time</th><th>Table</th><th>Result</th><th>P&amp;L</th>' +
        '</tr></thead><tbody id="hand-tbody">';
      for (var i = 0; i < hands.length; i++) {
        html += buildHandRow(hands[i]);
      }
      html += '</tbody></table>';

      // Page navigation
      html += '<div class="page-nav">';
      html += '<button class="page-nav-btn" id="page-prev"' + (currentPage === 0 ? ' disabled' : '') + '>&laquo; Prev</button>';
      html += '<span class="page-nav-info">Page ' + (currentPage + 1) + '</span>';
      html += '<button class="page-nav-btn" id="page-next"' + (!hasMore ? ' disabled' : '') + '>Next &raquo;</button>';
      html += '</div>';

      historyEl.innerHTML = html;
      attachHandListeners();
    }

    function goToPage(page) {
      currentPage = page;
      historyEl.innerHTML = '<div class="dash-empty">Loading...</div>';
      fetchHandPage(dashAgentId, pageCursors[page]).then(function (result) {
        renderHandHistory(dashAgentId, result.hands, result.hasMore, result.cursor);
      }).catch(function () {
        historyEl.innerHTML = '<div class="dash-empty">Failed to load hand history.</div>';
      });
    }

    function attachHandListeners() {
      // Click-to-expand rows
      var rows = document.querySelectorAll('.hand-row');
      for (var i = 0; i < rows.length; i++) {
        (function (row) {
          if (row.dataset.bound) return;
          row.dataset.bound = '1';
          row.addEventListener('click', function () {
            var handId = row.dataset.handId;
            var tableId = row.dataset.tableId;
            var detailRow = document.getElementById('detail-' + handId);
            if (!detailRow) return;

            var isOpen = detailRow.style.display !== 'none';
            if (isOpen) {
              detailRow.style.display = 'none';
              row.querySelector('.ht-toggle').textContent = '\u25B8';
              return;
            }

            detailRow.style.display = '';
            row.querySelector('.ht-toggle').textContent = '\u25BE';

            if (handDetailCache[handId]) {
              detailRow.querySelector('td').innerHTML = renderHandDetail(handDetailCache[handId], dashAgentId);
              return;
            }

            fetchHandDetail(tableId, handId).then(function (record) {
              detailRow.querySelector('td').innerHTML = renderHandDetail(record, dashAgentId);
            }).catch(function () {
              detailRow.querySelector('td').innerHTML = '<div class="hand-detail-inner text-dim">Failed to load hand details.</div>';
            });
          });
        })(rows[i]);
      }

      // Page navigation buttons
      var prevBtn = document.getElementById('page-prev');
      var nextBtn = document.getElementById('page-next');
      if (prevBtn) {
        prevBtn.addEventListener('click', function () {
          if (currentPage > 0) goToPage(currentPage - 1);
        });
      }
      if (nextBtn) {
        nextBtn.addEventListener('click', function () {
          if (pageHasMore) goToPage(currentPage + 1);
        });
      }
    }
  }
})();
