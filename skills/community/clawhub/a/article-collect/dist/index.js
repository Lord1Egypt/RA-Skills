import fs from "fs";
import path from "path";
import { getBrowser } from "@bondli-skills/shared/browser";
import { fetchUrlContent } from "./fetch-content.js";
const dbPath = path.join(process.env.HOME || "~", "/openclaw-skill-data/", "article-knowledge.json");
function loadDB() {
    if (!fs.existsSync(dbPath)) {
        // 如果文件不存在，创建文件
        const dir = path.dirname(dbPath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
        const emptyDB = { article: [] };
        fs.writeFileSync(dbPath, JSON.stringify(emptyDB, null, 2), "utf-8");
        console.log(`已创建数据库文件: ${dbPath}`);
        return emptyDB;
    }
    try {
        const content = fs.readFileSync(dbPath, "utf-8");
        return JSON.parse(content);
    }
    catch (error) {
        console.error(`读取数据库文件失败: ${error.message}`);
        console.log("返回空数据库结构");
        return { article: [] };
    }
}
function saveDB(db) {
    try {
        // 确保目录存在
        const dir = path.dirname(dbPath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
        fs.writeFileSync(dbPath, JSON.stringify(db, null, 2), "utf-8");
    }
    catch (error) {
        console.error(`保存数据库文件失败: ${error.message}`);
        throw error;
    }
}
const action = process.argv[2];
const url = process.argv[3];
const db = loadDB();
if (action === "add_article") {
    const exists = db.article.some(k => k.url === url);
    if (exists) {
        console.log("该 URL 已存在，跳过重复添加");
    }
    else {
        const browser = await getBrowser();
        const content = await fetchUrlContent(browser, url);
        db.article.push({
            url,
            summary: content,
            time: new Date().toISOString(),
        });
        saveDB(db);
        console.log("文章已保存");
    }
}
if (action === "list_article") {
    if (db.article.length === 0) {
        console.log("暂无文章记录");
        process.exit();
    }
    db.article.forEach((k, i) => {
        console.log(`${i + 1}. ${k.summary}`);
        console.log(`   ${k.url}`);
    });
    console.log(JSON.stringify(db.article));
}
if (action === "delete_article") {
    const index = parseInt(process.argv[3]) - 1;
    if (db.article[index]) {
        db.article.splice(index, 1);
        saveDB(db);
        console.log("文章记录已删除");
    }
    else {
        console.log("不存在该文章记录");
    }
}
process.exit(0);
//# sourceMappingURL=index.js.map