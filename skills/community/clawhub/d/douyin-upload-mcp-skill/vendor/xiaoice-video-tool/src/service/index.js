const { createHealthSnapshot } = require('../shared');
const { createVideoTaskService, startVideoTaskService } = require('./server');

function createServiceSkeleton() {
  return {
    name: 'video-task-service',
    health: createHealthSnapshot(),
  };
}

module.exports = {
  createServiceSkeleton,
  createVideoTaskService,
  startVideoTaskService,
};
