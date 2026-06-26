import { extractBlocks, getAttrValue, getTagText } from './xml-utils.mjs';

function getLocalName(block) {
  const m = String(block || '').match(/<\s*(?:\w+:)?(\w+)\b/);
  return m ? m[1] : '';
}

function parseNumber(value) {
  const parsed = Number.parseInt(String(value || ''), 10);
  return Number.isFinite(parsed) ? parsed : 0;
}

export function extractFolderBlocks(xml) {
  const names = [
    'Folder',
    'CalendarFolder',
    'ContactsFolder',
    'SearchFolder',
    'TasksFolder',
    'NotesFolder',
    'JournalFolder',
  ];

  const blocks = [];
  for (const name of names) {
    blocks.push(...extractBlocks(xml, name));
  }
  return blocks;
}

export function parseFolderBlock(block) {
  const folderType = getLocalName(block);
  const id =
    getAttrValue(block, 'FolderId', 'Id') ||
    getAttrValue(block, 'SearchFolderId', 'Id') ||
    '';
  const changeKey =
    getAttrValue(block, 'FolderId', 'ChangeKey') ||
    getAttrValue(block, 'SearchFolderId', 'ChangeKey') ||
    '';

  return {
    id,
    change_key: changeKey,
    folder_type: folderType,
    display_name: getTagText(block, 'DisplayName'),
    folder_class: getTagText(block, 'FolderClass'),
    parent_folder_id: getAttrValue(block, 'ParentFolderId', 'Id'),
    total_count: parseNumber(getTagText(block, 'TotalCount')),
    unread_count: parseNumber(getTagText(block, 'UnreadCount')),
    child_folder_count: parseNumber(getTagText(block, 'ChildFolderCount')),
  };
}
