// 显示创建模态框
function showCreateModal(parentUUID = '', project = '') {
    document.getElementById('createModal').style.display = 'flex';
    loadParentTasks(parentUUID);
    if (project) {
        document.getElementById('project').value = project;
    }
}

// 关闭创建模态框
function closeCreateModal() {
    document.getElementById('createModal').style.display = 'none';
    document.getElementById('createForm').reset();
    const parentSelect = document.getElementById('parentTask');
    if (parentSelect) {
        parentSelect.innerHTML = '<option value="">无（主任务）</option>';
    }
}

function loadParentTasks(selectedUUID = '') {
    const parentSelect = document.getElementById('parentTask');
    if (!parentSelect) {
        return;
    }
    fetch('/api/tasks?limit=1000')
        .then(r => r.json())
        .then(data => {
            parentSelect.innerHTML = '<option value="">无（主任务）</option>';
            if (!data.tasks) {
                return;
            }
            data.tasks
                .filter(task => !task.parent_uuid)
                .forEach(task => {
                    const option = document.createElement('option');
                    option.value = task.uuid;
                    option.textContent = task.project ? `${task.title} (${task.project})` : task.title;
                    parentSelect.appendChild(option);
                });
            if (selectedUUID) {
                parentSelect.value = selectedUUID;
            }
        });
}

// 创建任务
function createTask(event) {
    event.preventDefault();

    const title = document.getElementById('title').value.trim();
    const project = document.getElementById('project').value.trim();
    const parentUUID = document.getElementById('parentTask').value;

    if (!title) {
        alert('请输入任务标题');
        return;
    }

    if (!project) {
        alert('请输入项目名称');
        return;
    }

    const data = {
        title: title,
        description: document.getElementById('description').value,
        priority: parseInt(document.getElementById('priority').value),
        project: project,
        parent_uuid: parentUUID,
        assignee_name: document.getElementById('assignee').value,
        tags: document.getElementById('tags').value.split(',').map(t => t.trim()).filter(t => t)
    };
    
    fetch('/api/tasks', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(r => r.json())
    .then(result => {
        if (result.error) {
            alert('创建失败：' + result.error);
        } else {
            alert('任务创建成功！');
            closeCreateModal();
            window.location.reload();
        }
    })
    .catch(err => {
        alert('创建失败：' + err);
    });
}

// 更新任务状态
function updateStatus(uuid, status) {
    fetch(`/api/tasks/${uuid}/status`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({new_status: status})
    })
    .then(() => {
        window.location.reload();
    });
}

// 工具函数
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleString('zh-CN');
}

// 点击模态框外部关闭
window.onclick = function(event) {
    const modal = document.getElementById('createModal');
    if (event.target === modal) {
        closeCreateModal();
    }
}
