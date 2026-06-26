function createHealthSnapshot() {
  return {
    status: 'ok',
    version: 1,
  };
}

const {
  createVideoServiceClient,
  createTask,
  getTask,
  ServiceRequestError,
} = require('./video-service-client');

module.exports = {
  createHealthSnapshot,
  createVideoServiceClient,
  createTask,
  getTask,
  ServiceRequestError,
};
