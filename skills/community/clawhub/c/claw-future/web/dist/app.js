const state = {
  demo: false,
  accountId: '',
  accounts: [],
  tab: 'positions',
  direction: 'buy',
  offset: 'open',
  priceType: 'limit',
  quotes: new Map(),
  eventsCursor: 0,
  prepared: null,
  socket: null,
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
const money = (value, digits = 2) => value == null || Number.isNaN(Number(value)) ? '--' : Number(value).toLocaleString('zh-CN', {minimumFractionDigits: digits, maximumFractionDigits: digits});
const signed = (value) => value == null ? '--' : `${Number(value) >= 0 ? '+' : ''}${money(value)}`;
const uuid = () => (crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`);

async function api(path, options = {}) {
  const headers = {'Accept': 'application/json', ...(options.body ? {'Content-Type': 'application/json'} : {}), ...(options.headers || {})};
  const response = await fetch(path, {...options, headers});
  let payload;
  try { payload = await response.json(); } catch { payload = {ok: false, error: `HTTP ${response.status}`}; }
  if (!response.ok && !payload.error) payload.error = `HTTP ${response.status}`;
  return payload;
}

function toast(message, kind = 'info', detail = '') {
  const node = document.createElement('div');
  node.className = `toast ${kind}`;
  node.innerHTML = `<div>${escapeHtml(message)}</div>${detail ? `<small>${escapeHtml(detail)}</small>` : ''}`;
  $('#toastStack').append(node);
  setTimeout(() => node.remove(), 4800);
}

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>'"]/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
}

async function bootstrap() {
  bindLogin();
  const health = await api('/api/health');
  state.demo = Boolean(health.demo);
  $('#modeBadge').textContent = state.demo ? 'DEMO' : 'LIVE';
  const auth = await api('/api/auth/status');
  if (auth.required && !auth.authenticated) {
    $('#loginPanel').hidden = false;
    $('#loginToken').focus();
    return;
  }
  await loadWorkspace();
}

function bindLogin() {
  $('#loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const error = $('#loginError');
    error.textContent = '';
    const result = await api('/api/auth/login', {
      method: 'POST', body: JSON.stringify({token: $('#loginToken').value}),
    });
    if (!result.ok) { error.textContent = result.error || '令牌无效'; return; }
    $('#loginPanel').hidden = true;
    await loadWorkspace();
  });
}

async function loadWorkspace() {
  const accountResponse = await api('/api/accounts');
  if (!accountResponse.ok) { toast(accountResponse.error || '账户列表读取失败', 'error'); return; }
  state.accounts = accountResponse.accounts || [];
  populateAccounts();
  bindInteractions();
  await refreshAll();
  openStream();
}

function populateAccounts() {
  const select = $('#accountSelect');
  select.innerHTML = state.accounts.filter(item => item.enabled !== false).map(item => `<option value="${escapeHtml(item.account_id)}">${escapeHtml(item.display_name || item.account_id)}</option>`).join('');
  state.accountId = select.value || state.accounts[0]?.account_id || 'A';
  select.value = state.accountId;
  updateAccountLabels();
}

function updateAccountLabels() {
  const label = state.accounts.find(item => item.account_id === state.accountId)?.display_name || `账户 ${state.accountId}`;
  $('#ticketAccount').textContent = label;
  $('#ticketAccountFoot').textContent = state.accountId;
}

function bindInteractions() {
  $('#accountSelect').addEventListener('change', async (event) => {
    state.accountId = event.target.value;
    state.eventsCursor = 0;
    updateAccountLabels();
    closeStream();
    await refreshAll();
    openStream();
  });
  $('#refreshButton').addEventListener('click', refreshAll);
  $('#dataRefreshButton').addEventListener('click', refreshData);
  $('#orderForm').addEventListener('submit', prepareSubmit);
  $('#cancelConfirm').addEventListener('click', () => closeConfirm());
  $('#submitConfirm').addEventListener('click', submitPrepared);
  $('#instrumentSearch').addEventListener('input', renderQuotes);
  $('#subscribeButton').addEventListener('click', () => toast('订阅功能将在连接实例后生效', 'info'));
  $$('.direction-segment .segment').forEach(button => button.addEventListener('click', () => {
    state.direction = button.dataset.direction;
    $$('.direction-segment .segment').forEach(item => item.classList.toggle('active', item === button));
    updateOrderSummary();
  }));
  $$('.offset-segment .segment').forEach(button => button.addEventListener('click', () => {
    state.offset = button.dataset.offset;
    $$('.offset-segment .segment').forEach(item => item.classList.toggle('active', item === button));
    updateOrderSummary();
  }));
  $$('.mini-segment').forEach(button => button.addEventListener('click', () => {
    state.priceType = button.dataset.priceType;
    $$('.mini-segment').forEach(item => item.classList.toggle('active', item === button));
    $('#priceInput').disabled = state.priceType === 'market';
    $('#priceInput').style.opacity = state.priceType === 'market' ? '.55' : '1';
    updateOrderSummary();
  }));
  $$('[data-step]').forEach(button => button.addEventListener('click', () => {
    const input = $('#volumeInput'); input.value = Math.max(1, Number(input.value || 1) + Number(button.dataset.step)); updateOrderSummary();
  }));
  $$('[data-qty]').forEach(button => button.addEventListener('click', () => { $('#volumeInput').value = button.dataset.qty; updateOrderSummary(); }));
  $('#instrumentInput').addEventListener('input', updateOrderSummary);
  $('#volumeInput').addEventListener('input', updateOrderSummary);
  $('#priceInput').addEventListener('input', updateOrderSummary);
  $$('.tab').forEach(button => button.addEventListener('click', async () => {
    state.tab = button.dataset.tab; $$('.tab').forEach(item => item.classList.toggle('active', item === button)); await renderData();
  }));
}

async function refreshAll() {
  if (!state.accountId) return;
  await Promise.all([refreshStatus(), refreshFunds(), refreshQuotes(), refreshData()]);
}

async function refreshStatus() {
  const result = await api(`/api/accounts/${encodeURIComponent(state.accountId)}/status`);
  const badge = $('#connectionBadge');
  if (result.ok && result.settled) { badge.className = 'status-pill status-ok'; badge.innerHTML = '<i></i>已连接'; $('#accountState').textContent = '在线'; $('#accountStateDetail').textContent = '交易与行情正常'; }
  else if (result.ok) { badge.className = 'status-pill status-warn'; badge.innerHTML = '<i></i>待结算'; $('#accountState').textContent = '待结算'; $('#accountStateDetail').textContent = '等待交易确认'; }
  else { badge.className = 'status-pill status-error'; badge.innerHTML = '<i></i>未连接'; $('#accountState').textContent = '离线'; $('#accountStateDetail').textContent = result.error || '实例未运行'; }
  $('#tradingDay').textContent = `交易日 ${result.trading_day || '--'}`;
}

async function refreshFunds() {
  const result = await api(`/api/accounts/${encodeURIComponent(state.accountId)}/funds`);
  const account = result.account || {};
  $('#balanceValue').textContent = money(account.balance);
  $('#availableValue').textContent = money(account.available);
  $('#marginValue').textContent = money(account.margin);
  $('#frozenValue').textContent = `冻结 ${money(account.frozen_margin)}`;
  $('#profitValue').textContent = `当日盈亏 ${signed((account.position_profit || 0) + (account.close_profit || 0))}`;
  $('#positionProfitValue').textContent = signed(account.position_profit);
  $('#positionProfitValue').classList.toggle('positive', Number(account.position_profit) >= 0);
}

async function refreshQuotes() {
  const instruments = ['al2610', 'rb2701', 'au2612'];
  await Promise.all(instruments.map(async instrument => { const result = await api(`/api/accounts/${encodeURIComponent(state.accountId)}/quote?instrument=${encodeURIComponent(instrument)}`); if (result.ok && result.tick) state.quotes.set(instrument, result.tick); }));
  renderQuotes();
}

function renderQuotes() {
  const filter = ($('#instrumentSearch')?.value || '').trim().toLowerCase();
  const rows = [...state.quotes.values()].filter(tick => !filter || tick.instrument.toLowerCase().includes(filter));
  $('#quoteRows').innerHTML = rows.length ? rows.map(tick => {
    const change = (Number(tick.last) - Number(tick.pre_close)) / Number(tick.pre_close || 1) * 100;
    return `<tr class="quote-row" data-instrument="${escapeHtml(tick.instrument)}"><td><div class="contract-cell"><span class="contract-name">${escapeHtml(tick.instrument)}</span><span class="contract-exchange">${escapeHtml(tick.exchange || 'SHFE')}</span></div></td><td class="last-price">${money(tick.last)}</td><td class="${change >= 0 ? 'positive' : 'negative'}">${change >= 0 ? '+' : ''}${change.toFixed(2)}%</td><td class="book-cell">${money(tick.bid1)} <small>${tick.bid1_vol ?? '--'}</small></td><td class="book-cell">${money(tick.ask1)} <small>${tick.ask1_vol ?? '--'}</small></td><td>${Number(tick.vol || 0).toLocaleString()}</td><td><button class="row-action" data-fill="${escapeHtml(tick.instrument)}">填入</button></td></tr>`;
  }).join('') : '<tr><td class="empty-state" colspan="7">暂无行情</td></tr>';
  $$('.quote-row').forEach(row => row.addEventListener('click', () => fillFromQuote(row.dataset.instrument)));
  $$('.row-action').forEach(button => button.addEventListener('click', event => { event.stopPropagation(); fillFromQuote(button.dataset.fill); }));
  const latest = rows[0]; if (latest) $('#quoteUpdated').textContent = `更新 ${latest.update_time || '--'} · ${state.accountId}`;
}

function fillFromQuote(instrument) {
  const tick = state.quotes.get(instrument); if (!tick) return;
  $('#instrumentInput').value = instrument;
  $('#exchangeInput').value = tick.exchange || 'SHFE';
  $('#priceInput').value = state.direction === 'buy' ? tick.ask1 : tick.bid1;
  $('#priceHint').textContent = `${state.direction === 'buy' ? '卖一' : '买一'} ${money(state.direction === 'buy' ? tick.ask1 : tick.bid1)}`;
  updateOrderSummary(); $('#instrumentInput').focus(); toast(`${instrument} 已填入委托板`, 'success');
}

async function refreshData() {
  if (!state.accountId) return;
  const request = state.tab === 'positions' ? api(`/api/accounts/${encodeURIComponent(state.accountId)}/positions`) : state.tab === 'orders' ? api(`/api/accounts/${encodeURIComponent(state.accountId)}/orders`) : api(`/api/accounts/${encodeURIComponent(state.accountId)}/trades`);
  const result = await request; if (!result.ok) { renderDataError(result.error); return; }
  const items = result[state.tab] || []; renderData(items);
  if (state.tab === 'positions') $('#positionCount').textContent = items.length;
  if (state.tab === 'orders') $('#orderCount').textContent = items.length;
  if (state.tab === 'trades') $('#tradeCount').textContent = items.length;
}

function renderData(items = null) {
  if (items === null) { refreshData(); return; }
  const heads = {positions: ['合约', '方向', '持仓', '今仓 / 昨仓', '持仓成本', '保证金', '持仓盈亏', '操作'], orders: ['合约', '方向', '开平', '价格', '委托 / 成交', '状态', '时间', '操作'], trades: ['合约', '方向', '开平', '成交价', '手数', '成交时间', '委托号']};
  $('#dataHead').innerHTML = `<tr>${heads[state.tab].map(item => `<th>${item}</th>`).join('')}</tr>`;
  if (!items.length) { $('#dataRows').innerHTML = `<tr><td class="empty-state" colspan="${heads[state.tab].length}">暂无${state.tab === 'positions' ? '持仓' : state.tab === 'orders' ? '委托' : '成交'}</td></tr>`; return; }
  $('#dataRows').innerHTML = items.map(item => state.tab === 'positions' ? positionRow(item) : state.tab === 'orders' ? orderRow(item) : tradeRow(item)).join('');
  $$('.position-close').forEach(button => button.addEventListener('click', () => fillClose(button.dataset.instrument, button.dataset.direction)));
  $$('.cancel-order').forEach(button => button.addEventListener('click', () => cancelOne(button.dataset.ref, button.dataset.sysid, button.dataset.instrument)));
}

function positionRow(item) { const long = String(item.direction) === '2'; return `<tr><td class="contract-name">${escapeHtml(item.instrument)}</td><td class="${long ? 'positive' : 'negative'}">${long ? '多' : '空'}</td><td>${item.position ?? '--'}</td><td>${item.today_position ?? 0} / ${item.yd_position ?? 0}</td><td>${money(item.position_cost)}</td><td>${money(item.use_margin)}</td><td class="${Number(item.position_profit) >= 0 ? 'positive' : 'negative'}">${signed(item.position_profit)}</td><td><button class="text-button position-close" data-instrument="${escapeHtml(item.instrument)}" data-direction="${long ? 'sell' : 'buy'}">填入平仓</button></td></tr>`; }
function orderRow(item) { const buy = String(item.direction) === '0'; const active = !['0', '2', '4', '5', 'AllTraded', 'Canceled'].includes(String(item.order_status)); return `<tr><td class="contract-name">${escapeHtml(item.instrument)}</td><td class="${buy ? 'positive' : 'negative'}">${buy ? '买' : '卖'}</td><td>${String(item.offset) === '0' ? '开' : '平'}</td><td>${money(item.limit_price)}</td><td>${item.volume_traded ?? 0} / ${item.volume_total ?? 0}</td><td class="status-tag">${escapeHtml(item.status_msg || item.order_status || '--')}</td><td>${escapeHtml(item.insert_time || '--')}</td><td>${active ? `<button class="cancel-link cancel-order" data-ref="${escapeHtml(item.order_ref || '')}" data-sysid="${escapeHtml(item.order_sys_id || '')}" data-instrument="${escapeHtml(item.instrument || '')}">撤单</button>` : '<span class="muted">--</span>'}</td></tr>`; }
function tradeRow(item) { const buy = String(item.direction) === '0'; return `<tr><td class="contract-name">${escapeHtml(item.instrument)}</td><td class="${buy ? 'positive' : 'negative'}">${buy ? '买' : '卖'}</td><td>${String(item.offset) === '0' ? '开' : '平'}</td><td>${money(item.price)}</td><td>${item.volume ?? '--'}</td><td>${escapeHtml(item.trade_time || '--')}</td><td>${escapeHtml(item.order_ref || '--')}</td></tr>`; }
function renderDataError(error) { $('#dataHead').innerHTML = ''; $('#dataRows').innerHTML = `<tr><td class="empty-state" colspan="8">${escapeHtml(error || '读取失败')}</td></tr>`; }

function fillClose(instrument, direction) { $('#instrumentInput').value = instrument; state.direction = direction; state.offset = 'close'; $$('.direction-segment .segment').forEach(item => item.classList.toggle('active', item.dataset.direction === direction)); $$('.offset-segment .segment').forEach(item => item.classList.toggle('active', item.dataset.offset === 'close')); const tick = state.quotes.get(instrument); if (tick) $('#priceInput').value = direction === 'buy' ? tick.ask1 : tick.bid1; updateOrderSummary(); $('#instrumentInput').focus(); toast(`${instrument} 已填入平仓委托`, 'success'); }
function updateOrderSummary() { const instrument = $('#instrumentInput')?.value || '--'; const volume = Number($('#volumeInput')?.value || 1); const directionText = state.direction === 'buy' ? '买入' : '卖出'; const offsetText = {open: '开仓', close: '平仓', close_today: '平今', close_yesterday: '平昨'}[state.offset]; $('#orderSummary').textContent = `${directionText} · ${instrument} · ${offsetText} · ${volume} 手`; const price = state.priceType === 'market' ? 0 : Number($('#priceInput')?.value || 0); $('#estimatedValue').textContent = price ? `名义金额 ${money(price * volume)}` : '市价 · 以成交回报为准'; }

async function prepareSubmit(event) { event.preventDefault(); const order = {exchange: $('#exchangeInput').value, instrument: $('#instrumentInput').value.trim(), direction: state.direction, offset: state.offset, volume: Number($('#volumeInput').value), price_type: state.priceType, price: Number($('#priceInput').value || 0), time_cond: $('#timeCondInput').value, vol_cond: 'any'}; const result = await api(`/api/accounts/${encodeURIComponent(state.accountId)}/orders/prepare`, {method: 'POST', headers: {'X-Claw-Request': 'web'}, body: JSON.stringify(order)}); if (!result.ok) { toast(result.error || '委托校验失败', 'error'); return; } state.prepared = result; $('#confirmDetails').textContent = `${state.accountId} · ${order.instrument} · ${order.direction === 'buy' ? '买入' : '卖出'} ${order.offset === 'open' ? '开仓' : '平仓'} · ${order.volume} 手 · ${order.price_type === 'market' ? '市价' : `限价 ${money(order.price)}`}`; $('#confirmModal').hidden = false; $('#submitConfirm').focus(); }
function closeConfirm() { $('#confirmModal').hidden = true; state.prepared = null; }
async function submitPrepared() { if (!state.prepared) return; const button = $('#submitConfirm'); button.disabled = true; const result = await api(`/api/accounts/${encodeURIComponent(state.accountId)}/orders`, {method: 'POST', headers: {'X-Claw-Request': 'web'}, body: JSON.stringify({confirmation_token: state.prepared.confirmation_token, idempotency_key: `web-${uuid()}`})}); button.disabled = false; closeConfirm(); if (result.ok) { toast('委托已发送', 'success', `${state.accountId} · 委托号 ${result.order_ref || '--'}`); state.tab = 'orders'; $$('.tab').forEach(item => item.classList.toggle('active', item.dataset.tab === 'orders')); await refreshData(); } else toast(result.error || '委托发送失败', 'error'); }
async function cancelOne(orderRef, orderSysId, instrument) { const result = await api(`/api/accounts/${encodeURIComponent(state.accountId)}/orders/cancel`, {method: 'POST', headers: {'X-Claw-Request': 'web'}, body: JSON.stringify({idempotency_key: `web-cancel-${uuid()}`, order_ref: orderRef, order_sys_id: orderSysId, instrument})}); if (result.ok) { toast('撤单请求已发送', 'success', `${instrument} · ${orderRef}`); await refreshData(); } else toast(result.error || '撤单失败', 'error'); }

function openStream() { closeStream(); const protocol = location.protocol === 'https:' ? 'wss' : 'ws'; try { state.socket = new WebSocket(`${protocol}://${location.host}/ws/accounts/${encodeURIComponent(state.accountId)}?after_seq=${state.eventsCursor}`); state.socket.onmessage = event => { const payload = JSON.parse(event.data); if (payload.next_seq) state.eventsCursor = payload.next_seq; (payload.events || []).forEach(item => { if (item.type === 'tick' && item.tick) { state.quotes.set(item.tick.instrument, item.tick); renderQuotes(); } }); }; state.socket.onclose = () => { if (state.accountId) setTimeout(() => { if (!state.socket || state.socket.readyState === WebSocket.CLOSED) openStream(); }, 1500); }; } catch { /* polling fallback is handled by refresh */ } }
function closeStream() { if (state.socket) { state.socket.onclose = null; state.socket.close(); state.socket = null; } }

bootstrap().catch(error => toast(error.message || '工作台初始化失败', 'error'));
