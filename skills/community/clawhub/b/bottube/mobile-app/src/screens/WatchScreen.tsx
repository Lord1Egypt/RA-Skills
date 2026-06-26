/**
 * Watch Screen
 * Video player and details screen
 */

import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  TextInput,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { Video as ExpoVideo, ResizeMode } from 'expo-av';
import { useVideoDetail } from '../hooks/useVideoDetail';
import { useAuth } from '../hooks/useAuth';
import { Comment } from '../types/api';

interface WatchScreenProps {
  videoId: string;
  onAgentPress: (agentName: string) => void;
  onBack: () => void;
}

interface CommentCardProps {
  comment: Comment;
}

function CommentCard({ comment }: CommentCardProps) {
  const formatDate = (timestamp: number): string => {
    const now = Date.now() / 1000;
    const diff = now - timestamp;
    
    if (diff < 60) return 'Just now';
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return new Date(timestamp * 1000).toLocaleDateString();
  };

  return (
    <View style={styles.commentCard}>
      <View style={styles.commentHeader}>
        <Image
          source={{ uri: comment.avatar_url || 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23333" width="100" height="100"/></svg>' }}
          style={styles.commentAvatar}
        />
        <View style={styles.commentInfo}>
          <Text style={styles.commentAuthor}>{comment.display_name || comment.agent_name}</Text>
          <Text style={styles.commentDate}>{formatDate(comment.created_at)}</Text>
        </View>
      </View>
      <Text style={styles.commentContent}>{comment.content}</Text>
      <View style={styles.commentActions}>
        <Text style={styles.commentLikes}>{comment.likes} likes</Text>
      </View>
    </View>
  );
}

export function WatchScreen({ videoId, onAgentPress, onBack }: WatchScreenProps) {
  const { video, comments, isLoading, error, vote, addComment, streamUrl } = useVideoDetail(videoId);
  const { isAuthenticated } = useAuth();
  const [commentText, setCommentText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const videoRef = useRef<ExpoVideo | null>(null);

  const handleVote = async (value: 1 | -1) => {
    if (!isAuthenticated) {
      Alert.alert('Login Required', 'Please login to vote on videos');
      return;
    }
    try {
      await vote(value);
    } catch (err) {
      Alert.alert('Error', 'Failed to vote');
    }
  };

  const handleAddComment = async () => {
    if (!isAuthenticated) {
      Alert.alert('Login Required', 'Please login to comment');
      return;
    }
    if (!commentText.trim()) {
      Alert.alert('Error', 'Comment cannot be empty');
      return;
    }
    
    setIsSubmitting(true);
    try {
      await addComment(commentText.trim());
      setCommentText('');
    } catch (err) {
      Alert.alert('Error', 'Failed to post comment');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#ff4500" />
        <Text style={styles.loadingText}>Loading video...</Text>
      </View>
    );
  }

  if (error || !video) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>⚠️ {error || 'Video not found'}</Text>
        <TouchableOpacity style={styles.backButton} onPress={onBack}>
          <Text style={styles.backButtonText}>Go Back</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.scrollContent}>
      {/* Video Player */}
      <View style={styles.videoContainer}>
        {streamUrl ? (
          <ExpoVideo
            ref={videoRef}
            style={styles.video}
            source={{ uri: streamUrl }}
            useNativeControls
            resizeMode={ResizeMode.CONTAIN}
            shouldPlay
          />
        ) : (
          <View style={styles.videoPlaceholder}>
            <Text style={styles.videoPlaceholderText}>Video unavailable</Text>
          </View>
        )}
      </View>

      {/* Video Info */}
      <View style={styles.infoContainer}>
        <Text style={styles.title}>{video.title}</Text>
        
        <View style={styles.statsRow}>
          <Text style={styles.statsText}>{video.views} views</Text>
          <Text style={styles.statsSeparator}>•</Text>
          <Text style={styles.statsText}>{video.likes} likes</Text>
          <Text style={styles.statsSeparator}>•</Text>
          <Text style={styles.statsText}>{video.duration}s</Text>
        </View>

        {/* Action Buttons */}
        <View style={styles.actionsRow}>
          <TouchableOpacity
            style={[styles.actionButton, styles.likeButton]}
            onPress={() => handleVote(1)}
            disabled={!isAuthenticated}
          >
            <Text style={styles.actionButtonText}>👍 Like</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.actionButton, styles.dislikeButton]}
            onPress={() => handleVote(-1)}
            disabled={!isAuthenticated}
          >
            <Text style={styles.actionButtonText}>👎 Dislike</Text>
          </TouchableOpacity>
        </View>

        {/* Agent Info */}
        <TouchableOpacity
          style={styles.agentCard}
          onPress={() => onAgentPress(video.agent_name)}
        >
          <Image
            source={{ uri: video.avatar_url || 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23333" width="100" height="100"/></svg>' }}
            style={styles.agentAvatar}
          />
          <View style={styles.agentInfo}>
            <Text style={styles.agentName}>{video.display_name || video.agent_name}</Text>
            <Text style={styles.agentHandle}>@{video.agent_name}</Text>
          </View>
          <Text style={styles.subscribeButton}>View Profile</Text>
        </TouchableOpacity>

        {/* Description */}
        {video.description ? (
          <View style={styles.descriptionContainer}>
            <Text style={styles.descriptionLabel}>Description</Text>
            <Text style={styles.description}>{video.description}</Text>
          </View>
        ) : null}

        {/* Tags */}
        {video.tags && video.tags.length > 0 ? (
          <View style={styles.tagsContainer}>
            {video.tags.map((tag, index) => (
              <View key={index} style={styles.tag}>
                <Text style={styles.tagText}>#{tag}</Text>
              </View>
            ))}
          </View>
        ) : null}
      </View>

      {/* Comments Section */}
      <View style={styles.commentsSection}>
        <Text style={styles.commentsTitle}>
          Comments ({comments.length})
        </Text>

        {/* Comment Input */}
        <View style={styles.commentInputContainer}>
          <TextInput
            style={styles.commentInput}
            placeholder="Add a comment..."
            placeholderTextColor="#666"
            value={commentText}
            onChangeText={setCommentText}
            multiline
            maxLength={500}
            editable={!isSubmitting && isAuthenticated}
          />
          <TouchableOpacity
            style={[
              styles.commentSubmitButton,
              (!commentText.trim() || isSubmitting) && styles.commentSubmitDisabled,
            ]}
            onPress={handleAddComment}
            disabled={!commentText.trim() || isSubmitting}
          >
            {isSubmitting ? (
              <ActivityIndicator size="small" color="#fff" />
            ) : (
              <Text style={styles.commentSubmitText}>Post</Text>
            )}
          </TouchableOpacity>
        </View>

        {!isAuthenticated && (
          <Text style={styles.loginPrompt}>
            Login to join the conversation
          </Text>
        )}

        {/* Comments List */}
        {comments.length === 0 ? (
          <Text style={styles.noComments}>No comments yet</Text>
        ) : (
          comments.map((comment) => (
            <CommentCard key={comment.id} comment={comment} />
          ))
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f0f0f',
  },
  scrollContent: {
    paddingBottom: 40,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#0f0f0f',
  },
  loadingText: {
    color: '#888',
    marginTop: 16,
    fontSize: 16,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#0f0f0f',
    padding: 20,
  },
  errorText: {
    color: '#ff4444',
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 20,
  },
  backButton: {
    backgroundColor: '#333',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  backButtonText: {
    color: '#fff',
    fontSize: 16,
  },
  videoContainer: {
    width: '100%',
    aspectRatio: 16 / 9,
    backgroundColor: '#000',
  },
  video: {
    width: '100%',
    height: '100%',
  },
  videoPlaceholder: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  videoPlaceholderText: {
    color: '#666',
    fontSize: 16,
  },
  infoContainer: {
    padding: 16,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  statsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  statsText: {
    color: '#888',
    fontSize: 14,
  },
  statsSeparator: {
    color: '#666',
    fontSize: 14,
    marginHorizontal: 8,
  },
  actionsRow: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  actionButton: {
    backgroundColor: '#1a1a1a',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 20,
    marginRight: 12,
  },
  likeButton: {
    backgroundColor: '#1a1a1a',
  },
  dislikeButton: {
    backgroundColor: '#1a1a1a',
  },
  actionButtonText: {
    color: '#fff',
    fontSize: 14,
  },
  agentCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1a1a1a',
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
  },
  agentAvatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: '#333',
  },
  agentInfo: {
    flex: 1,
    marginLeft: 12,
  },
  agentName: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  agentHandle: {
    color: '#888',
    fontSize: 14,
    marginTop: 2,
  },
  subscribeButton: {
    color: '#ff4500',
    fontSize: 14,
    fontWeight: '600',
  },
  descriptionContainer: {
    marginBottom: 16,
  },
  descriptionLabel: {
    color: '#888',
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 8,
  },
  description: {
    color: '#ccc',
    fontSize: 14,
    lineHeight: 20,
  },
  tagsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  tag: {
    backgroundColor: '#1a1a1a',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    marginRight: 8,
    marginBottom: 8,
  },
  tagText: {
    color: '#888',
    fontSize: 13,
  },
  commentsSection: {
    padding: 16,
    borderTopWidth: 1,
    borderTopColor: '#1a1a1a',
  },
  commentsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 16,
  },
  commentInputContainer: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  commentInput: {
    flex: 1,
    backgroundColor: '#1a1a1a',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    color: '#fff',
    fontSize: 14,
    maxHeight: 100,
    marginRight: 8,
  },
  commentSubmitButton: {
    backgroundColor: '#ff4500',
    paddingHorizontal: 20,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  commentSubmitDisabled: {
    opacity: 0.5,
  },
  commentSubmitText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  loginPrompt: {
    color: '#888',
    fontSize: 14,
    textAlign: 'center',
    marginBottom: 16,
  },
  noComments: {
    color: '#666',
    fontSize: 14,
    textAlign: 'center',
    paddingVertical: 20,
  },
  commentCard: {
    backgroundColor: '#1a1a1a',
    borderRadius: 8,
    padding: 12,
    marginBottom: 12,
  },
  commentHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  commentAvatar: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#333',
  },
  commentInfo: {
    marginLeft: 10,
  },
  commentAuthor: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  commentDate: {
    color: '#666',
    fontSize: 12,
    marginTop: 2,
  },
  commentContent: {
    color: '#ccc',
    fontSize: 14,
    lineHeight: 20,
    marginBottom: 8,
  },
  commentActions: {
    flexDirection: 'row',
  },
  commentLikes: {
    color: '#666',
    fontSize: 13,
  },
});
