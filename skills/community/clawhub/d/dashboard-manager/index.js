/** 
 * SKILL: Dashboard Manager 
 * Description: Gère les interactions avec le dashboard Jarvis 
 * 
 * Ce skill permet de : 
 * - Lire le fichier data.json 
 * - Mettre à jour le fichier data.json 
 * - Récupérer les notes pending 
 * - Marquer les notes comme processed 
 * - Ajouter des logs et mettre à jour les stats 
 */
const fs = require('fs').promises;
const path = require('path');

// Configuration - MODIFIE CE CHEMIN SELON TON INSTALLATION
const DATA_FILE_PATH = 'D:\\Projets\\ClaudBot\\Jarvis_Dashboard\\data.json';

/** 
 * Charge la base de données depuis data.json 
 */
async function loadDatabase() {
    try {
        const data = await fs.readFile(DATA_FILE_PATH, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error('❌ Erreur lors de la lecture de data.json:', error.message);
        throw error;
    }
}

/** 
 * Sauvegarde la base de données dans data.json 
 */
async function saveDatabase(db) {
    try {
        await fs.writeFile( 
            DATA_FILE_PATH, 
            JSON.stringify(db, null, 2), 
            'utf8' 
        );
        console.log('✅ Base de données sauvegardée');
        return true;
    } catch (error) {
        console.error('❌ Erreur lors de la sauvegarde de data.json:', error.message);
        throw error;
    }
}

/** 
 * Récupère les notes en attente (status = "pending") 
 */
async function getPendingNotes() {
    const db = await loadDatabase();
    const pendingNotes = (db.quick_notes || []).filter( note => note.status === 'pending' );
    console.log(`📩 ${pendingNotes.length} note(s) en attente`);
    return pendingNotes;
}

/** 
 * Marque une note comme "processed" 
 */
async function processNote(noteId) {
    const db = await loadDatabase();
    const note = db.quick_notes?.find(n => n.id === noteId);
    if (note) {
        note.status = 'processed';
        await saveDatabase(db);
        console.log(`✅ Note #${noteId} marquée comme traitée`);
        return true;
    }
    console.warn(`⚠️ Note #${noteId} introuvable`);
    return false;
}

/** 
 * Ajoute un log dans l'historique 
 */
async function addLog(action) {
    const db = await loadDatabase();
    const now = new Date();
    const time = now.toLocaleString('fr-FR', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
    const newLog = { time: time, action: action };
    if (!db.logs) db.logs = [];
    db.logs.unshift(newLog); // Ajoute au début
    await saveDatabase(db);
    console.log(`📝 Log ajouté: ${action}`);
    return true;
}

/** 
 * Met à jour le statut du système 
 */
async function updateSystemStatus(state = 'idle', modelName = null) {
    const db = await loadDatabase();
    const now = new Date();
    const timestamp = now.toLocaleString('fr-FR', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
    if (!db.system_status) db.system_status = {};
    db.system_status.state = state;
    db.system_status.last_heartbeat = timestamp;
    if (modelName) {
        db.system_status.current_model = modelName;
    }
    await saveDatabase(db);
    console.log(`⚡ Système mis à jour: ${state}`);
    return true;
}

/** 
 * Met à jour les statistiques de tokens et coûts 
 */
async function updateStats(inputTokens, outputTokens, cost) {
    const db = await loadDatabase();
    if (!db.stats) db.stats = { input_tokens: 0, output_tokens: 0, total_cost: 0 };
    // Incrémente les compteurs
    db.stats.input_tokens = (db.stats.input_tokens || 0) + inputTokens;
    db.stats.output_tokens = (db.stats.output_tokens || 0) + outputTokens;
    db.stats.total_cost = (db.stats.total_cost || 0) + cost;
    await saveDatabase(db);
    console.log(`💰 Stats mises à jour: +${inputTokens} tokens in, +${outputTokens} tokens out, +$${cost.toFixed(4)}`);
    return true;
}

/** 
 * Ajoute ou met à jour une tâche 
 */
async function updateTask(taskId, updates) {
    const db = await loadDatabase();
    if (!db.tasks) db.tasks = [];
    const task = db.tasks.find(t => t.id === taskId);
    if (task) {
        // Met à jour la tâche existante
        Object.assign(task, updates);
        console.log(`✏️ Tâche #${taskId} mise à jour`);
    } else {
        // Crée une nouvelle tâche
        const newTask = { id: taskId || (db.tasks.length + 1), ...updates };
        db.tasks.push(newTask);
        console.log(`➕ Nouvelle tâche créée: ${newTask.text}`);
    }
    await saveDatabase(db);
    return true;
}

/** 
 * Ajoute un sub-agent actif 
 */
async function addSubAgent(agentName, task = null) {
    const db = await loadDatabase();
    if (!db.system_status) db.system_status = {};
    if (!db.system_status.sub_agents_active) db.system_status.sub_agents_active = [];
    const agent = { name: agentName, task: task, started_at: new Date().toISOString() };
    db.system_status.sub_agents_active.push(agent);
    await saveDatabase(db);
    console.log(`🤖 Sub-agent ajouté: ${agentName}`);
    return true;
}

/** 
 * Retire un sub-agent actif 
 */
async function removeSubAgent(agentName) {
    const db = await loadDatabase();
    if (!db.system_status?.sub_agents_active) return false;
    db.system_status.sub_agents_active = db.system_status.sub_agents_active.filter( 
        agent => agent.name !== agentName 
    );
    await saveDatabase(db);
    console.log(`🔴 Sub-agent retiré: ${agentName}`);
    return true;
}

// Export des fonctions pour OpenClaw
module.exports = {
    name: 'dashboard-manager',
    description: 'Gère les interactions avec le dashboard Jarvis',
    version: '1.0.0',
    
    // Fonctions principales
    functions: {
        loadDatabase,
        saveDatabase,
        getPendingNotes,
        processNote,
        addLog,
        updateSystemStatus,
        updateStats,
        updateTask,
        addSubAgent,
        removeSubAgent
    },
    
    // Fonction d'initialisation
    async init() {
        console.log('🚀 Dashboard Manager skill initialisé');
        console.log(`📁 Chemin du fichier: ${DATA_FILE_PATH}`);
        
        // Teste si le fichier est accessible
        try {
            await loadDatabase();
            console.log('✅ Connexion au dashboard établie');
            return true;
        } catch (error) {
            console.error('❌ Impossible de se connecter au dashboard');
            console.error(' Vérifie que le fichier existe:', DATA_FILE_PATH);
            return false;
        }
    }
};