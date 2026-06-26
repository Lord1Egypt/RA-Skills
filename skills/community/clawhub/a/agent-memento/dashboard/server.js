const express = require('express');
const cors = require('cors');
const chokidar = require('chokidar');
const path = require('path');
const fs = require('fs');
const { WebSocketServer } = require('ws');
const { exec, execFile } = require('child_process');
const minimist = require('minimist');

const argv = minimist(process.argv.slice(2));
const PROJECT_DIR = argv['project-dir'] ? path.resolve(argv['project-dir']) : path.resolve('../projects/demo');
const PORT = argv['port'] || 3777;

const ENABLE_PREVIEW = argv['enable-preview'] || false;
const HOST = argv['host'] || '127.0.0.1'; // Default to localhost for security


const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Opt-in mount of the user project directory as a static preview path
if (ENABLE_PREVIEW) {
    app.use('/preview', express.static(PROJECT_DIR));
} else {
    app.use('/preview', (req, res) => res.status(403).send('Preview disabled for security. Start dashboard with --enable-preview to view.'));
}


// File paths
const PLAN_PATH = path.join(PROJECT_DIR, 'docs', 'MASTER_PLAN.md');
const STATUS_PATH = path.join(PROJECT_DIR, 'docs', 'TICK_STATUS.md');
const NOTES_PATH = path.join(PROJECT_DIR, 'docs', 'HUMAN_NOTES.md');
const MAP_PATH = path.join(PROJECT_DIR, 'docs', 'PROJECT_MAP.md');
const LOGS_DIR = path.join(PROJECT_DIR, 'logs');

// Ensure files exist
const ensureFiles = () => {
    [PLAN_PATH, STATUS_PATH, NOTES_PATH, MAP_PATH].forEach(f => {
        if (!fs.existsSync(f)) {
            fs.mkdirSync(path.dirname(f), { recursive: true });
            fs.writeFileSync(f, '');
        }
    });
};
ensureFiles();

// REST API
app.get('/api/plan', (req, res) => {
    res.json({ content: fs.readFileSync(PLAN_PATH, 'utf-8') });
});
app.get('/api/status', (req, res) => {
    res.json({ content: fs.readFileSync(STATUS_PATH, 'utf-8') });
});
app.get('/api/notes', (req, res) => {
    res.json({ content: fs.readFileSync(NOTES_PATH, 'utf-8') });
});
app.get('/api/map', (req, res) => {
    res.json({ content: fs.readFileSync(MAP_PATH, 'utf-8') });
});

// Update Tick Mode
app.post('/api/plan/control', (req, res) => {
    const { mode } = req.body;
    let content = fs.readFileSync(PLAN_PATH, 'utf-8');
    content = content.replace(/tick_mode:\s*\w+/, `tick_mode: ${mode}`);
    fs.writeFileSync(PLAN_PATH, content);
    res.json({ success: true, mode });
});

// Add Note
app.post('/api/notes', (req, res) => {
    const { target, text } = req.body;
    const now = new Date().toISOString().replace('Z', '');
    const entry = `\n### [NOTE] ${now} → ${target}\n${text}\n`;
    
    let content = fs.readFileSync(NOTES_PATH, 'utf-8');
    if (content.includes('## Active Notes')) {
        content = content.replace('## Active Notes', `## Active Notes\n${entry}`);
    } else {
        content += entry;
    }
    fs.writeFileSync(NOTES_PATH, content);
    res.json({ success: true });
});

// Chat to LLM via OpenClaw
app.post('/api/chat', (req, res) => {
    const message = req.body.message || '';
    if (!message) return res.status(400).json({ error: 'empty message' });

    const sessionName = `memento-dashboard-${path.basename(PROJECT_DIR)}`;
    
    // Instead of passing everything via a fragile bash command line string, we rely on the JS process.env
    const planData = fs.existsSync(PLAN_PATH) ? fs.readFileSync(PLAN_PATH, 'utf-8') : '';
    
    const prompt = `You are the Architect of a Memento autonomous project. You reside in the Dashboard and act as a Supervisor.
The user is talking to you to check progress, steer the project, or answer questions. 
CRITICAL RULE:
1. DO NOT pause or stop the project unless explicitly told to do so.
2. DO NOT ask the user "should I proceed?" or wait for confirmation. The actual coding work is done in the background automatically by a cron job running the Tick engine. 
3. If the user asks "is it finished" or "how is it going", just read and summarize the MASTER_PLAN state below. Do NOT attempt to edit or rewrite the MASTER_PLAN file unless the user EXPLICITLY asks to change the requirements, add tasks, or modify the goals.
4. Keep your replies very brief, decisive, and conversational. Do not use the file editing tool unprompted.

Here is the current MASTER_PLAN.md state:
${planData}

User Command: ${message}`;
    
    const tmpOut = path.join(require('os').tmpdir(), 'arch_out_' + Date.now() + '.json');
    const cmdFiles = path.join(require('os').tmpdir(), 'arch_prompt_' + Date.now() + '.txt');
    fs.writeFileSync(cmdFiles, prompt);
    
    // For security compliance: 
    // DO NOT spread process.env to the child agent to prevent AWS/GCP credential leakage. 
    // We only pass the bare minimum PATH needed to run openclaw.
    const secureEnv = { PATH: process.env.PATH || '/usr/bin:/bin:/usr/local/bin' };

    // Run it, and write all stdout to tmpOut
    // Using execFile with bash to prevent variable injection from user strings
    const cmdArgs = [
        '-c',
        `openclaw agent --local --json --session-id "$1" -m "$(cat "$2")" > "$3" 2>&1`,
        '--',
        sessionName,
        cmdFiles,
        tmpOut
    ];

    execFile('bash', cmdArgs, { timeout: 120000, env: secureEnv }, (error, stdout, stderr) => {
        try {
            const d = fs.readFileSync(tmpOut, 'utf8');
            let p = null;

            // Simple robust regex search: look for {"payloads":[{"text": ...}]} 
            // Since there can be multiple huge JSON chunks from tracking, 
            // instead of matching strings, we will just isolate EVERY valid { ... } and parse it looking for "payloads".
            
            p = { payloads: [{text: ""}] };
            
            // extract everything that looks like a JSON line containing payloads (often formatted nicely in --json)
            try {
                // Find all lines containing "payloads": [
                const lines = d.split('\n');
                let foundJsonText = "";
                let inJson = false;
                for (let line of lines) {
                    if (line.trim().startsWith('{"meta":')) {
                        inJson = true;
                        foundJsonText = line; // maybe single line JSON?
                        if (line.includes('"payloads":[') && !line.includes('"tools":[')) {
                            // telemetry dumps usually contain "total":... or "metrics"... 
                            // Standard output from agent usually has {"meta":{...},"payloads":[{"text":"...
                            let parsed = JSON.parse(line);
                            if(parsed.payloads && parsed.payloads[0].text) {
                                p = parsed;
                            }
                        }
                    }
                }
            } catch(ex) {
                // fallback to regex
            }

            if (!p.payloads[0].text) {
                // Hard regex fallback
                let finalMatch = d.match(/"text"\s*:\s*"((?:\\.|[^"\\])*)"/g);
                if (finalMatch && finalMatch.length > 0) {
                    let lastStr = finalMatch[finalMatch.length - 1]; // usually the final output
                    let theText = JSON.parse("{" + lastStr + "}").text;
                    p.payloads[0].text = theText;
                } else {
                     throw new Error('Fallback regex regex failed to find text key.');
                }
            } 
            
            // cleanup
            fs.unlinkSync(tmpOut);
            fs.unlinkSync(cmdFiles);

            res.json({ reply: p.payloads[0].text, color: '#8ad7ff' });
        } catch (e) {
            console.error("Parse Error:", e.message);
            // let's try to grab whatever raw text from the error
            let rawLines = [];
            try { rawLines = fs.readFileSync(tmpOut, 'utf8').split('\n').slice(-10); } catch(x){}
            res.json({ reply: '【系统桥接失败】\n' + rawLines.join('\n').substring(0,200), color: '#ff8a8a' });
        }
    });
});

// Create Server & WSS
const server = app.listen(PORT, HOST, () => {
    console.log(`🧠 Agent Memento Dashboard running at http://${HOST}:${PORT}`);
    console.log(`📁 Watching project directory: ${PROJECT_DIR}`);
});

const wss = new WebSocketServer({ server, path: '/ws/events' });

wss.on('connection', (ws) => {
    ws.send(JSON.stringify({ type: 'connected' }));
});

const broadcast = (data) => {
    wss.clients.forEach(client => {
        if (client.readyState === 1) { // OPEN
            client.send(JSON.stringify(data));
        }
    });
};

// Watch file changes
const watcher = chokidar.watch([PLAN_PATH, STATUS_PATH, NOTES_PATH, MAP_PATH], {
    persistent: true,
    ignoreInitial: true,
    awaitWriteFinish: { stabilityThreshold: 500, pollInterval: 100 }
});

watcher.on('change', (filePath) => {
    const basename = path.basename(filePath);
    let type = 'unknown';
    if (basename === 'MASTER_PLAN.md') type = 'plan_updated';
    else if (basename === 'TICK_STATUS.md') type = 'status_updated';
    else if (basename === 'HUMAN_NOTES.md') type = 'notes_updated';
    else if (basename === 'PROJECT_MAP.md') type = 'map_updated';

    broadcast({ type, file: basename });
});
