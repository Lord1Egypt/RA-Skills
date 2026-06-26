// ============================================================
//  Adaptive Learning Engine — FSRS + BKT
//  Uses ts-fsrs (UMD global: window.ts_fsrs)
// ============================================================

const FSRS_LIB = window.FSRS || window.ts_fsrs;
const { createEmptyCard, fsrs, Rating, State } = FSRS_LIB;

// ===== AVAILABLE COURSES (register here or load dynamically) =====
const COURSE_REGISTRY = [
  { id: 'cs170', name: 'CS 170', desc: 'Efficient Algorithms & Intractable Problems', school: 'UC Berkeley', term: 'Spring 2026' }
  // Add more courses here
];

// ===== STORAGE KEYS =====
const STORE_PREFIX = 'alearn_';
const storeKey = (courseId, key) => `${STORE_PREFIX}${courseId}_${key}`;

// ===== APP STATE =====
const App = {
  courseId: null,
  courseMeta: null,
  questions: [],
  allTopics: [],

  // FSRS scheduler
  scheduler: null,
  retention: 0.9,
  dailyNew: 20,

  // Per-card FSRS state: { [qid]: { card: FSRSCard, log: [] } }
  cardStates: {},

  // BKT per-topic: { [topic]: { mastery: float, history: [{correct, ts}] } }
  topicMastery: {},

  // Session
  mode: 'breadth',
  depthTopicIdx: 0,
  currentQ: null,
  flipped: false,
  sessionStats: { seen: 0, correct: 0 },
  newToday: 0,
  todayKey: new Date().toISOString().slice(0, 10),

  // ===== INIT =====
  init() {
    this.renderCourseSelector();
    this.setupDropZone();
    this.setupKeyboard();

    // Auto-load if URL has ?course=xxx
    const params = new URLSearchParams(location.search);
    const cid = params.get('course');
    if (cid) this.loadCourse(cid);
  },

  // ===== COURSE SELECTOR =====
  renderCourseSelector() {
    const list = document.getElementById('course-list');
    // Check which courses have saved data
    const cards = COURSE_REGISTRY.map(c => {
      const saved = localStorage.getItem(storeKey(c.id, 'questions'));
      const hasSave = localStorage.getItem(storeKey(c.id, 'cards'));
      let qCount = '';
      if (saved) {
        try { qCount = ` (${JSON.parse(saved).length} 题)`; } catch(e) {}
      }
      return `<div class="course-card" onclick="App.loadCourse('${c.id}')">
        <h3>${c.name}</h3>
        <div class="meta">${c.school}${c.term ? ' · ' + c.term : ''}</div>
        <div class="topic-count">${saved ? '✅ 题库已加载' + qCount : '📦 点击加载'}${hasSave ? ' · 📝 有学习记录' : ''}</div>
      </div>`;
    });
    list.innerHTML = cards.join('') || '<p style="color:var(--text-dim)">暂无课程，请拖入 questions.json</p>';
  },

  setupDropZone() {
    const zone = document.getElementById('drop-zone');
    const input = document.getElementById('file-input');
    zone.onclick = () => input.click();
    zone.ondragover = e => { e.preventDefault(); zone.classList.add('drag-over'); };
    zone.ondragleave = () => zone.classList.remove('drag-over');
    zone.ondrop = e => {
      e.preventDefault(); zone.classList.remove('drag-over');
      const file = e.dataTransfer.files[0];
      if (file) this.importFile(file);
    };
    input.onchange = e => { if (e.target.files[0]) this.importFile(e.target.files[0]); };
  },

  async importFile(file) {
    try {
      const text = await file.text();
      const data = JSON.parse(text);
      // Detect format: array of questions or {course, questions}
      let questions, courseId, courseName;
      if (Array.isArray(data)) {
        questions = data;
        courseId = 'custom_' + Date.now();
        courseName = file.name.replace('.json', '');
      } else {
        questions = data.questions || data;
        courseId = data.id || 'custom_' + Date.now();
        courseName = data.name || file.name.replace('.json', '');
      }
      localStorage.setItem(storeKey(courseId, 'questions'), JSON.stringify(questions));
      // Register if not already
      if (!COURSE_REGISTRY.find(c => c.id === courseId)) {
        COURSE_REGISTRY.push({ id: courseId, name: courseName, desc: '', school: '', term: '' });
      }
      this.renderCourseSelector();
      this.loadCourse(courseId);
    } catch (e) {
      alert('JSON 解析失败: ' + e.message);
    }
  },

  // ===== LOAD COURSE =====
  async loadCourse(courseId) {
    this.courseId = courseId;
    this.courseMeta = COURSE_REGISTRY.find(c => c.id === courseId) || { name: courseId };

    // Try loading questions from localStorage first, then from file
    let qData = localStorage.getItem(storeKey(courseId, 'questions'));
    if (!qData) {
      // Try loading from courses/<id>/questions.json
      try {
        const resp = await fetch(`../courses/${courseId}/questions.json`);
        if (resp.ok) {
          const questions = await resp.json();
          localStorage.setItem(storeKey(courseId, 'questions'), JSON.stringify(questions));
          qData = JSON.stringify(questions);
        }
      } catch (e) {}
    }

    if (!qData) {
      alert('找不到该课程的题库，请先导入 questions.json');
      return;
    }

    this.questions = JSON.parse(qData);
    this.allTopics = [...new Set(this.questions.map(q => q.topic))];
    this.allTopics.sort((a, b) => {
      const ai = this.questions.find(q => q.topic === a)?.topicIndex ?? 99;
      const bi = this.questions.find(q => q.topic === b)?.topicIndex ?? 99;
      return ai - bi;
    });

    // Init FSRS scheduler
    this.initFSRS();

    // Load saved state
    this.loadState();

    // Switch screens
    document.getElementById('course-selector').style.display = 'none';
    document.getElementById('learn-screen').style.display = '';
    document.getElementById('course-title').textContent = '📚 ' + this.courseMeta.name;

    // Update URL
    history.replaceState(null, '', '?course=' + courseId);

    this.nextQuestion();
  },

  initFSRS() {
    this.scheduler = fsrs({ request_retention: this.retention });
  },

  // ===== STATE PERSISTENCE =====
  saveState() {
    const data = {
      mode: this.mode,
      depthTopicIdx: this.depthTopicIdx,
      retention: this.retention,
      dailyNew: this.dailyNew,
      cardStates: {},
      topicMastery: this.topicMastery,
      sessionStats: this.sessionStats,
      newToday: this.newToday,
      todayKey: this.todayKey,
    };
    // Serialize FSRS card states
    for (const [qid, cs] of Object.entries(this.cardStates)) {
      data.cardStates[qid] = {
        card: {
          due: cs.card.due.toISOString ? cs.card.due.toISOString() : cs.card.due,
          stability: cs.card.stability,
          difficulty: cs.card.difficulty,
          elapsed_days: cs.card.elapsed_days,
          scheduled_days: cs.card.scheduled_days,
          reps: cs.card.reps,
          lapses: cs.card.lapses,
          state: cs.card.state,
          last_review: cs.card.last_review ? (cs.card.last_review.toISOString ? cs.card.last_review.toISOString() : cs.card.last_review) : undefined,
        },
        ratings: cs.ratings || [],
      };
    }
    localStorage.setItem(storeKey(this.courseId, 'cards'), JSON.stringify(data));
  },

  loadState() {
    try {
      const raw = localStorage.getItem(storeKey(this.courseId, 'cards'));
      if (!raw) return;
      const data = JSON.parse(raw);
      this.mode = data.mode || 'breadth';
      this.depthTopicIdx = data.depthTopicIdx || 0;
      this.retention = data.retention || 0.9;
      this.dailyNew = data.dailyNew || 20;
      this.topicMastery = data.topicMastery || {};
      this.sessionStats = data.sessionStats || { seen: 0, correct: 0 };
      this.newToday = data.newToday || 0;
      this.todayKey = data.todayKey || new Date().toISOString().slice(0, 10);

      // Reset daily counter if new day
      const today = new Date().toISOString().slice(0, 10);
      if (this.todayKey !== today) {
        this.newToday = 0;
        this.todayKey = today;
      }

      // Restore FSRS card states
      this.cardStates = {};
      for (const [qid, cs] of Object.entries(data.cardStates || {})) {
        const c = cs.card;
        this.cardStates[qid] = {
          card: {
            due: new Date(c.due),
            stability: c.stability,
            difficulty: c.difficulty,
            elapsed_days: c.elapsed_days,
            scheduled_days: c.scheduled_days,
            reps: c.reps,
            lapses: c.lapses,
            state: c.state,
            last_review: c.last_review ? new Date(c.last_review) : undefined,
          },
          ratings: cs.ratings || [],
        };
      }

      // Restore UI
      this.scheduler = fsrs({ request_retention: this.retention });
      document.querySelectorAll('.mode-btn').forEach(b => b.classList.toggle('active', b.dataset.mode === this.mode));
      document.getElementById('retention-slider').value = this.retention;
      document.getElementById('retention-val').textContent = Math.round(this.retention * 100) + '%';
      document.getElementById('daily-new').value = this.dailyNew;
    } catch (e) {
      console.error('Failed to load state:', e);
    }
  },

  // ===== FSRS CARD MANAGEMENT =====
  getCardState(qid) {
    if (!this.cardStates[qid]) {
      this.cardStates[qid] = {
        card: createEmptyCard(new Date()),
        ratings: [],
      };
    }
    return this.cardStates[qid];
  },

  isNew(qid) {
    return !this.cardStates[qid] || this.cardStates[qid].card.reps === 0;
  },

  isDue(qid) {
    const cs = this.cardStates[qid];
    if (!cs) return true; // new = due
    return new Date(cs.card.due) <= new Date();
  },

  // ===== BKT (Simplified Bayesian Knowledge Tracing) =====
  updateBKT(topic, correct) {
    const P_T = 0.1;   // transition: probability of learning per attempt
    const P_S = 0.05;  // slip: know it but answer wrong
    const P_G = 0.25;  // guess: don't know but answer right

    if (!this.topicMastery[topic]) {
      this.topicMastery[topic] = { mastery: 0.1, attempts: 0, correct: 0 };
    }
    const tm = this.topicMastery[topic];
    let P_L = tm.mastery;

    // Bayesian update
    if (correct) {
      P_L = (P_L * (1 - P_S)) / (P_L * (1 - P_S) + (1 - P_L) * P_G);
    } else {
      P_L = (P_L * P_S) / (P_L * P_S + (1 - P_L) * (1 - P_G));
    }
    // Learning transition
    P_L = P_L + (1 - P_L) * P_T;

    tm.mastery = Math.min(Math.max(P_L, 0.01), 0.99);
    tm.attempts++;
    if (correct) tm.correct++;
  },

  getTopicMastery(topic) {
    return this.topicMastery[topic]?.mastery || 0.1;
  },

  // ===== QUESTION SELECTION =====
  nextQuestion() {
    this.flipped = false;
    const q = this.mode === 'breadth' ? this.pickBreadth() : this.pickDepth();

    if (!q) {
      document.getElementById('card-inner').innerHTML =
        '<div class="empty-state"><div class="emoji">🎉</div><p>太棒了！暂时没有需要复习的卡片。</p><p style="margin-top:8px;font-size:14px">过段时间再回来看看</p></div>';
      document.getElementById('rating-btns').style.display = 'none';
      document.getElementById('extra-btns').style.display = 'none';
      this.updateUI();
      return;
    }
    this.currentQ = q;
    this.renderCard();
    this.updateUI();
  },

  pickBreadth() {
    const now = new Date();

    // Priority 1: Due reviews (sorted by overdue-ness)
    const dueCards = this.questions.filter(q => {
      const cs = this.cardStates[q.id];
      return cs && cs.card.reps > 0 && new Date(cs.card.due) <= now;
    }).sort((a, b) => {
      return new Date(this.cardStates[a.id].card.due) - new Date(this.cardStates[b.id].card.due);
    });

    // In breadth mode, prefer due cards from weakest topics first
    if (dueCards.length > 0) {
      dueCards.sort((a, b) => this.getTopicMastery(a.topic) - this.getTopicMastery(b.topic));
      return dueCards[0];
    }

    // Priority 2: New cards (limited by dailyNew), from weakest topics, lowest difficulty first
    if (this.newToday < this.dailyNew) {
      const newCards = this.questions.filter(q => this.isNew(q.id));
      if (newCards.length > 0) {
        // Sort: weakest topic first, then by difficulty ascending
        newCards.sort((a, b) => {
          const mDiff = this.getTopicMastery(a.topic) - this.getTopicMastery(b.topic);
          if (Math.abs(mDiff) > 0.05) return mDiff;
          if (a.topicIndex !== b.topicIndex) return a.topicIndex - b.topicIndex;
          return a.difficulty - b.difficulty;
        });
        return newCards[0];
      }
    }

    return null; // All done for now
  },

  pickDepth() {
    const topic = this.allTopics[this.depthTopicIdx % this.allTopics.length];
    const now = new Date();

    // Due reviews in this topic first
    const dueInTopic = this.questions.filter(q =>
      q.topic === topic && this.cardStates[q.id] && this.cardStates[q.id].card.reps > 0
      && new Date(this.cardStates[q.id].card.due) <= now
    ).sort((a, b) => new Date(this.cardStates[a.id].card.due) - new Date(this.cardStates[b.id].card.due));

    if (dueInTopic.length > 0) return dueInTopic[0];

    // New cards in this topic
    if (this.newToday < this.dailyNew) {
      const newInTopic = this.questions.filter(q => q.topic === topic && this.isNew(q.id))
        .sort((a, b) => a.difficulty - b.difficulty);
      if (newInTopic.length > 0) return newInTopic[0];
    }

    // Nothing in this topic? Check other topics for due
    const dueOther = this.questions.filter(q =>
      this.cardStates[q.id] && this.cardStates[q.id].card.reps > 0
      && new Date(this.cardStates[q.id].card.due) <= now
    ).sort((a, b) => new Date(this.cardStates[a.id].card.due) - new Date(this.cardStates[b.id].card.due));

    return dueOther.length > 0 ? dueOther[0] : null;
  },

  // ===== CARD RENDERING =====
  renderCard() {
    const q = this.currentQ;
    if (!q) return;
    const diffLabels = { 1: '基础', 2: '中等', 3: '高级' };
    const cs = this.getCardState(q.id);
    const isReview = cs.card.reps > 0;

    let fsrsInfo = '';
    if (isReview) {
      const s = cs.card.stability?.toFixed(1) || '?';
      const d = cs.card.difficulty?.toFixed(1) || '?';
      fsrsInfo = `<span class="fsrs-tag">S:${s} D:${d}</span>`;
    } else {
      fsrsInfo = '<span class="fsrs-tag">新卡片</span>';
    }

    let html = `
      <div class="card-badge">
        <span class="topic-tag">${q.topic}</span>
        <span class="diff-tag diff-${q.difficulty}">${diffLabels[q.difficulty] || '?'}</span>
        ${fsrsInfo}
      </div>
      <div class="card-content">${this.formatText(q.question)}</div>
    `;

    if (this.flipped) {
      html += `
        <hr class="card-divider">
        <div>
          <div class="answer-label">答案</div>
          <div class="card-content">${this.formatText(q.answer)}</div>
        </div>
      `;
    } else {
      html += '<div class="card-hint">点击查看答案 →</div>';
    }

    document.getElementById('card-inner').innerHTML = html;
    document.getElementById('rating-btns').style.display = this.flipped ? 'flex' : 'none';

    const extraBtns = document.getElementById('extra-btns');
    const followupBtn = document.getElementById('btn-followup');
    const nextTopicBtn = document.getElementById('btn-next-topic');
    if (this.flipped) {
      extraBtns.style.display = 'flex';
      followupBtn.style.display = this.mode === 'breadth' ? 'inline-flex' : 'none';
      nextTopicBtn.style.display = this.mode === 'depth' ? 'inline-flex' : 'none';
    } else {
      extraBtns.style.display = 'none';
    }

    // Render KaTeX
    setTimeout(() => {
      renderMathInElement(document.getElementById('card-inner'), {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false },
          { left: '\\[', right: '\\]', display: true },
          { left: '\\(', right: '\\)', display: false }
        ],
        throwOnError: false
      });
    }, 10);
  },

  formatText(text) {
    return (text || '').replace(/\\n/g, '<br>').replace(/\n/g, '<br>');
  },

  flip() {
    if (this.flipped || !this.currentQ) return;
    this.flipped = true;
    this.renderCard();
  },

  // ===== RATING =====
  rate(ratingName) {
    const q = this.currentQ;
    if (!q) return;

    const ratingMap = { good: Rating.Good, hard: Rating.Hard, again: Rating.Again };
    const rating = ratingMap[ratingName] || Rating.Good;
    const correct = ratingName === 'good';

    const cs = this.getCardState(q.id);
    const wasNew = cs.card.reps === 0;

    // FSRS scheduling
    const now = new Date();
    const result = this.scheduler.next(cs.card, now, rating);
    cs.card = result.card;
    cs.ratings.push({ rating: ratingName, ts: now.toISOString() });
    this.cardStates[q.id] = cs;

    // BKT update
    this.updateBKT(q.topic, correct);

    // Stats
    this.sessionStats.seen++;
    if (correct) this.sessionStats.correct++;
    if (wasNew) this.newToday++;

    this.saveState();
    this.nextQuestion();
  },

  // ===== ACTIONS =====
  followUp() {
    if (!this.currentQ) return;
    const topic = this.currentQ.topic;
    const diff = this.currentQ.difficulty;
    const candidates = this.questions.filter(q =>
      q.topic === topic && q.id !== this.currentQ.id && this.isNew(q.id)
      && Math.abs(q.difficulty - diff) <= 1
    );
    if (candidates.length > 0) {
      this.currentQ = candidates[0];
      this.flipped = false;
      this.renderCard();
      this.updateUI();
    } else {
      // Try any unseen in same topic
      const fallback = this.questions.filter(q => q.topic === topic && q.id !== this.currentQ.id && this.isNew(q.id));
      if (fallback.length > 0) {
        this.currentQ = fallback[0];
        this.flipped = false;
        this.renderCard();
        this.updateUI();
      }
    }
  },

  nextTopic() {
    this.depthTopicIdx = (this.depthTopicIdx + 1) % this.allTopics.length;
    this.saveState();
    this.nextQuestion();
  },

  // ===== MODE =====
  setMode(m) {
    this.mode = m;
    document.querySelectorAll('.mode-btn').forEach(b => b.classList.toggle('active', b.dataset.mode === m));
    this.saveState();
    this.nextQuestion();
  },

  // ===== SETTINGS =====
  setRetention(val) {
    this.retention = parseFloat(val);
    document.getElementById('retention-val').textContent = Math.round(this.retention * 100) + '%';
    this.scheduler = fsrs({ request_retention: this.retention });
    this.saveState();
  },

  setDailyNew(val) {
    this.dailyNew = parseInt(val) || 20;
    this.saveState();
  },

  // ===== UI UPDATES =====
  updateUI() {
    const now = new Date();
    const dueCount = this.questions.filter(q => {
      const cs = this.cardStates[q.id];
      return cs && cs.card.reps > 0 && new Date(cs.card.due) <= now;
    }).length;
    const newCount = this.questions.filter(q => this.isNew(q.id)).length;

    document.getElementById('stat-due').textContent = `📋 ${dueCount} 待复习`;
    document.getElementById('stat-seen').textContent = `已学: ${this.questions.length - newCount}/${this.questions.length}`;

    const acc = this.sessionStats.seen > 0
      ? Math.round(this.sessionStats.correct / this.sessionStats.seen * 100) : '--';
    document.getElementById('stat-retention').textContent = `正确率: ${acc}%`;

    if (this.currentQ) {
      document.getElementById('progress-topic').textContent = `📖 ${this.currentQ.topic}`;
      const diffLabels = { 1: '基础', 2: '中等', 3: '高级' };
      document.getElementById('progress-diff').textContent = `难度: ${diffLabels[this.currentQ.difficulty] || '?'}`;
    }

    const total = this.questions.length;
    const learned = this.questions.filter(q => !this.isNew(q.id)).length;
    document.getElementById('progress-fill').style.width = `${Math.round(learned / total * 100)}%`;

    this.updateDrawer();
  },

  updateDrawer() {
    const list = document.getElementById('topic-list');
    list.innerHTML = this.allTopics.map(t => {
      const tm = this.topicMastery[t];
      let scoreClass = 'score-none', scoreText = '未开始';
      if (tm && tm.attempts > 0) {
        const m = tm.mastery;
        if (m >= 0.7) { scoreClass = 'score-high'; scoreText = `${Math.round(m * 100)}%`; }
        else if (m >= 0.4) { scoreClass = 'score-mid'; scoreText = `${Math.round(m * 100)}%`; }
        else { scoreClass = 'score-low'; scoreText = `${Math.round(m * 100)}%`; }
      }
      return `<div class="topic-item">
        <span>${t}</span>
        <span class="topic-score ${scoreClass}">${scoreText}</span>
      </div>`;
    }).join('');
  },

  toggleDrawer() {
    document.getElementById('drawer').classList.toggle('open');
    document.getElementById('drawer-overlay').classList.toggle('open');
  },

  // ===== NAVIGATION =====
  backToCourses() {
    document.getElementById('learn-screen').style.display = 'none';
    document.getElementById('course-selector').style.display = '';
    history.replaceState(null, '', location.pathname);
    this.renderCourseSelector();
  },

  resetCourse() {
    if (!confirm('确定要重置该课程的所有学习记录？')) return;
    localStorage.removeItem(storeKey(this.courseId, 'cards'));
    this.cardStates = {};
    this.topicMastery = {};
    this.sessionStats = { seen: 0, correct: 0 };
    this.newToday = 0;
    this.depthTopicIdx = 0;
    this.nextQuestion();
  },

  // ===== KEYBOARD =====
  setupKeyboard() {
    document.addEventListener('keydown', e => {
      if (document.getElementById('learn-screen').style.display === 'none') return;
      if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); this.flip(); }
      if (this.flipped) {
        if (e.key === '1') this.rate('good');
        if (e.key === '2') this.rate('hard');
        if (e.key === '3') this.rate('again');
        if (e.key === 'f' && this.mode === 'breadth') this.followUp();
        if (e.key === 'n' && this.mode === 'depth') this.nextTopic();
      }
    });
  },
};

// ===== BOOT =====
App.init();
