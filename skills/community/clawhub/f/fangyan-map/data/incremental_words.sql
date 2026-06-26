-- 增量方言词库（每次 init_db.py 会自动执行）
-- 格式：INSERT OR IGNORE（自动跳过已存在的记录）
-- 使用方法：往这个文件里追加新词即可

-- [2026-06-07] 徐哥添加
INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES ('哈尔滨话', '动词', '撬', '别', '撬锁、撬门，东北话一般说"别锁"、"把门别开"');
INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES ('哈尔滨话', '动词', '撬门锁', '别门锁', '撬门锁，东北话一般说"别门锁"');
INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES ('哈尔滨话', '形容词', '冷门', '嘎咕', '形容事物很生僻、很偏门');
INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES ('哈尔滨话', '形容词', '偏门', '嘎咕', '形容事物很生僻、很偏门');
INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES ('哈尔滨话', '形容词', '生僻', '嘎咕', '形容事物很生僻、很偏门');
INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES ('哈尔滨话', '形容词', '嘎咕', '冷门', '嘎咕是哈尔滨话，意思是冷门、偏门、生僻');
INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES ('哈尔滨话', '动词', '找东西', '撒磨', '找东西、搜寻，东北话也叫"撒磨"');
INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES ('哈尔滨话', '动词', '找东西', '穴么', '找东西、搜寻，东北话也叫"穴么"');
INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES ('哈尔滨话', '形容词', '反应慢', '卡愣', '脑子慢、反应迟钝、办事不灵光，熟人调侃为主');
INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES ('哈尔滨话', '动词', '瞎扯', '扯犊子', '话瞎、吹牛、不干正事，熟人调侃，不伤和气');
INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES ('哈尔滨话', '形容词', '没本事', '土卡拉', '能力弱、没出息、啥也不是，偏贬义');
INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES ('哈尔滨话', '形容词', '能力差', '土卡拉', '能力弱、没出息、啥也不是，偏贬义');
INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES ('哈尔滨话', '形容词', '窝囊', '土卡拉', '能力弱、没出息、啥也不是，偏贬义');
INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES ('哈尔滨话', '动词', '说话', '吱声', '吭声、说话，如「你吱一声啊」');
